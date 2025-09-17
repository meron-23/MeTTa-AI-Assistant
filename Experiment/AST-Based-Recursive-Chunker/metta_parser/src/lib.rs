use core::ops::Range;
use pyo3::prelude::*;
use std::io;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[pyclass]
pub enum SyntaxNodeType {
    Comment,
    VariableToken,
    StringToken,
    WordToken,
    OpenParen,
    CloseParen,
    Whitespace,
    LeftoverText,
    ExpressionGroup,
    ErrorGroup,
}

impl SyntaxNodeType {
    pub fn is_leaf(&self) -> bool {
        match self {
            Self::ExpressionGroup | Self::ErrorGroup => false,
            _ => true,
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
#[pyclass]
pub struct SyntaxNode {
    #[pyo3(get)]
    pub node_type: SyntaxNodeType,
    #[pyo3(get)]
    pub sub_nodes: Vec<SyntaxNode>,
    #[pyo3(get)]
    pub parsed_text: Option<String>,
    #[pyo3(get)]
    pub message: Option<String>,
    #[pyo3(get)]
    pub is_complete: bool,

    // Not directly exposed, but used by the src_range getter
    src_range_internal: Range<usize>,
}

#[pymethods]
impl SyntaxNode {
    // The byte range [start, end) in the source text.
    #[getter]
    fn src_range(&self) -> (usize, usize) {
        (self.src_range_internal.start, self.src_range_internal.end)
    }

    fn __str__(&self) -> String {
        format!(
            "SyntaxNode(type={:?}, range=({:?}), text={:?})",
            self.node_type,
            self.src_range(),
            self.parsed_text
        )
    }

    fn __repr__(&self) -> String {
        self.__str__()
    }
}

// Internal Rust implementation of SyntaxNode
impl SyntaxNode {
    fn new(node_type: SyntaxNodeType, src_range: Range<usize>, sub_nodes: Vec<SyntaxNode>) -> Self {
        Self {
            node_type,
            src_range_internal: src_range,
            sub_nodes,
            parsed_text: None,
            message: None,
            is_complete: true,
        }
    }

    fn new_token_node(node_type: SyntaxNodeType, src_range: Range<usize>, text: String) -> Self {
        let mut node = Self::new(node_type, src_range, vec![]);
        node.parsed_text = Some(text);
        node
    }
}

// Parser Logic (Internal to Rust)
struct CharReader<R: Iterator<Item = io::Result<char>>> {
    it: R,
    idx: usize,
    peeked: (Option<(usize, io::Result<char>)>, usize),
}
impl<R: Iterator<Item = io::Result<char>>> CharReader<R> {
    fn new(it: R) -> Self {
        let mut s = Self {
            it,
            idx: 0,
            peeked: (None, 0),
        };
        s.peeked = s.next_internal();
        s
    }
    fn last_idx(&self) -> usize {
        self.idx
    }
    fn peek(&self) -> Option<&(usize, io::Result<char>)> {
        self.peeked.0.as_ref()
    }
    fn next(&mut self) -> Option<(usize, io::Result<char>)> {
        self.idx += self.peeked.1;
        let next = self.next_internal();
        std::mem::replace(&mut self.peeked, next).0
    }
    fn next_internal(&mut self) -> (Option<(usize, io::Result<char>)>, usize) {
        match self.it.next() {
            Some(Ok(c)) => (Some((self.idx, Ok(c))), c.len_utf8()),
            Some(Err(e)) => (Some((self.idx, Err(e))), 0),
            None => (None, 0),
        }
    }
}
impl<'a> From<&'a str>
    for CharReader<std::iter::Map<std::str::Chars<'a>, fn(char) -> io::Result<char>>>
{
    fn from(text: &'a str) -> Self {
        Self::new(text.chars().map(Ok))
    }
}

struct SExprParser<'a> {
    it: CharReader<std::iter::Map<std::str::Chars<'a>, fn(char) -> io::Result<char>>>,
}

impl<'a> SExprParser<'a> {
    fn new(text: &'a str) -> Self {
        Self { it: text.into() }
    }
    fn peek(&self) -> Result<Option<(usize, char)>, String> {
        match self.it.peek() {
            Some(&(idx, Ok(c))) => Ok(Some((idx, c))),
            None => Ok(None),
            Some((idx, Err(e))) => Err(format!("Read error at {}: {}", idx, e)),
        }
    }
    fn next(&mut self) -> Result<Option<(usize, char)>, String> {
        match self.it.next() {
            Some((idx, Ok(c))) => Ok(Some((idx, c))),
            None => Ok(None),
            Some((idx, Err(e))) => Err(format!("Read error at {}: {}", idx, e)),
        }
    }
    fn skip_next(&mut self) {
        self.it.next();
    }
    fn cur_idx(&self) -> usize {
        self.it.last_idx()
    }

    // This is the main parsing function that gets called repeatedly.
    fn parse_to_syntax_tree(&mut self) -> Result<Option<SyntaxNode>, String> {
        while let Some((_, c)) = self.peek()? {
            // Skip leading whitespace, but return it as a node if needed by a caller
            if c.is_whitespace() {
                self.skip_next();
                continue; // We loop to find the next meaningful token
            }
            // Now parse the actual content
            return match c {
                '!' => self.parse_exec_expression().map(Some),
                ';' => self.parse_comment(),
                '$' => self.parse_variable().map(Some),
                '(' => self.parse_expr().map(Some),
                ')' => Err("Unexpected ')' at top level".to_string()),
                '"' => self.parse_string().map(Some),
                _ => self.parse_word().map(Some),
            };
        }
        Ok(None) // End of stream
    }

    fn parse_exec_expression(&mut self) -> Result<SyntaxNode, String> {
        let start_idx = self.cur_idx();

        // parse the '!' as a WordToken.
        let bang_node = self.parse_word()?;

        while let Some((_, c)) = self.peek()? {
            if c.is_whitespace() {
                self.skip_next();
            } else {
                break;
            }
        }

        let expr_node = match self.peek()? {
            Some((_, '(')) => self.parse_expr()?,
            _ => return Err("Expected an expression after '!'".to_string()),
        };

        // We label it ExpressionGroup because syntactically it is one unit.
        let children = vec![bang_node, expr_node];
        Ok(SyntaxNode::new(
            SyntaxNodeType::ExpressionGroup,
            start_idx..self.cur_idx(),
            children,
        ))
    }

    fn parse_comment(&mut self) -> Result<Option<SyntaxNode>, String> {
        let start_idx = self.cur_idx();
        self.skip_next(); // Consume ';'
        while let Some((_, c)) = self.peek()? {
            if c == '\n' {
                break;
            }
            self.skip_next();
        }
        let node = SyntaxNode::new(SyntaxNodeType::Comment, start_idx..self.cur_idx(), vec![]);
        Ok(Some(node))
    }

    fn parse_expr(&mut self) -> Result<SyntaxNode, String> {
        let start_idx = self.cur_idx();
        let mut children = vec![];

        children.push(SyntaxNode::new(
            SyntaxNodeType::OpenParen,
            start_idx..start_idx + 1,
            vec![],
        ));
        self.skip_next(); // Consume '('

        loop {
            // Skip internal whitespace/comments
            while let Some((_, c)) = self.peek()? {
                if c.is_whitespace() {
                    self.skip_next();
                    continue;
                }
                if c == ';' {
                    if let Some(comment) = self.parse_comment()? {
                        children.push(comment);
                    }
                    continue;
                }
                break;
            }

            if let Some((idx, c)) = self.peek()? {
                match c {
                    ')' => {
                        children.push(SyntaxNode::new(
                            SyntaxNodeType::CloseParen,
                            idx..idx + 1,
                            vec![],
                        ));
                        self.skip_next(); // Consume ')'
                        return Ok(SyntaxNode::new(
                            SyntaxNodeType::ExpressionGroup,
                            start_idx..self.cur_idx(),
                            children,
                        ));
                    }
                    _ => {
                        // Recursively parse child nodes
                        if let Some(child) = self.parse_to_syntax_tree()? {
                            children.push(child);
                        } else {
                            // This case should ideally not be hit if input is well-formed
                            return Err("Unexpected end of input inside expression".to_string());
                        }
                    }
                }
            } else {
                return Err("Unclosed expression".to_string());
            }
        }
    }

    // Simplified parse_string, parse_word, parse_variable methods...
    fn parse_string(&mut self) -> Result<SyntaxNode, String> {
        let start_idx = self.cur_idx();
        let mut text = String::new();
        self.skip_next(); // Consume opening '"'
        while let Some((_, c)) = self.peek()? {
            self.skip_next();
            if c == '"' {
                break;
            }
            text.push(c);
        }
        Ok(SyntaxNode::new_token_node(
            SyntaxNodeType::StringToken,
            start_idx..self.cur_idx(),
            text,
        ))
    }

    fn parse_word(&mut self) -> Result<SyntaxNode, String> {
        let start_idx = self.cur_idx();
        let mut text = String::new();
        while let Some((_, c)) = self.peek()? {
            if c.is_whitespace() || "();".contains(c) {
                break;
            }
            text.push(c);
            self.skip_next();
        }
        Ok(SyntaxNode::new_token_node(
            SyntaxNodeType::WordToken,
            start_idx..self.cur_idx(),
            text,
        ))
    }

    fn parse_variable(&mut self) -> Result<SyntaxNode, String> {
        let start_idx = self.cur_idx();
        let mut text = String::new();
        self.skip_next(); // Consume '$'
        while let Some((_, c)) = self.peek()? {
            if c.is_whitespace() || "();".contains(c) {
                break;
            }
            text.push(c);
            self.skip_next();
        }
        Ok(SyntaxNode::new_token_node(
            SyntaxNodeType::VariableToken,
            start_idx..self.cur_idx(),
            text,
        ))
    }
}

/// Parses MeTTa code and returns a list of top-level syntax nodes.
#[pyfunction]
fn parse(code: &str) -> PyResult<Vec<SyntaxNode>> {
    let mut parser = SExprParser::new(code);
    let mut roots = Vec::new();
    while let Some(node) = parser
        .parse_to_syntax_tree()
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e))?
    {
        roots.push(node);
    }
    Ok(roots)
}

/// A Python module implemented in Rust.
#[pymodule]
fn metta_parser(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    m.add_class::<SyntaxNode>()?;
    m.add_class::<SyntaxNodeType>()?;
    Ok(())
}
