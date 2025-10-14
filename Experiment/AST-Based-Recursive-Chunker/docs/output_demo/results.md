```lisp
(.venv) ➜  AST-Based-Recursive-Chunker git:(contained-chunk) ✗ python3 chunker.py data/raw_metta_programs/tree.metta data/output_chunks/tree.metta --max-size 1000
Reading from 'data/raw_metta_programs/tree.metta'...
Chunking code with MAX_SIZE = 1000...
;; =========================
{'type': 'def', 'symbol': 'comment_0'}
node_id: 1
;; TYPE SIGNATURES GROUPED
{'type': 'def', 'symbol': 'comment_1'}
node_id: 2
;; =========================
{'type': 'def', 'symbol': 'comment_2'}
node_id: 3
(: Tree (-> $a Type))
{'type': 'type', 'symbol': 'Tree'}
node_id: 4
(: mkTree (-> (Node $a) (List (Tree $a)) (Tree $a)))
{'type': 'type', 'symbol': 'mkTree'}
node_id: 5
(: Node (-> $a Type))
{'type': 'type', 'symbol': 'Node'}
node_id: 6
(: mkNode (-> $a (Node $a)))
{'type': 'type', 'symbol': 'mkNode'}
node_id: 7
(: NullVertex (Tree $a))
{'type': 'type', 'symbol': 'NullVertex'}
node_id: 8
(: mkNullVex (-> (List (Tree $a)) (Tree $a)))
{'type': 'type', 'symbol': 'mkNullVex'}
node_id: 9
(: getNodeValue (-> (Tree $a) (Node $a)))
{'type': 'type', 'symbol': 'getNodeValue'}
node_id: 10
(: getChildren (-> (Tree $a) (List (Tree $a))))
{'type': 'type', 'symbol': 'getChildren'}
node_id: 11
(: updateChildren (-> (Tree $a) (List (Tree $a)) (Tree $a)))
{'type': 'type', 'symbol': 'updateChildren'}
node_id: 12
(: preOrder (-> (Tree $a) $a))
{'type': 'type', 'symbol': 'preOrder'}
node_id: 13
(: buildTree (-> $a (Tree $a)))
{'type': 'type', 'symbol': 'buildTree'}
node_id: 14
(: cleanTree (-> (Tree $a) (Tree $a)))
{'type': 'type', 'symbol': 'cleanTree'}
node_id: 15
;; Get an id of a certain node. And (0) if the root node.
{'type': 'def', 'symbol': 'comment_15'}
node_id: 16
;; Example:
{'type': 'def', 'symbol': 'comment_16'}
node_id: 17
;;    Id of A in the (AND (OR (AND A B))) => (1 1 1)
{'type': 'def', 'symbol': 'comment_17'}
node_id: 18
;;    Id of (AND A B) in the (AND (OR (AND A B))) => (1 1)
{'type': 'def', 'symbol': 'comment_18'}
node_id: 19
;; Params:
{'type': 'def', 'symbol': 'comment_19'}
node_id: 20
;;   $tree: The full tree to search
{'type': 'def', 'symbol': 'comment_20'}
node_id: 21
;;   $targetTree: The target tree to find the ID of.
{'type': 'def', 'symbol': 'comment_21'}
node_id: 22
;; Returns:
{'type': 'def', 'symbol': 'comment_22'}
node_id: 23
;;   NodeId: The id of the targetTree if found.
{'type': 'def', 'symbol': 'comment_23'}
node_id: 24
(: getNodeId (-> (Tree $a) (Tree $a) NodeId))
{'type': 'type', 'symbol': 'getNodeId'}
node_id: 25
(: getNodeId (-> (Tree $a) (Tree $a) NodeId NodeId))
{'type': 'type', 'symbol': 'getNodeId'}
node_id: 26
;; Helper function for the getNodeId function.
{'type': 'def', 'symbol': 'comment_26'}
node_id: 27
;;   The function's sole purpose is to make the
{'type': 'def', 'symbol': 'comment_27'}
node_id: 28
;;   getNodeById compatible for the foldr function call.
{'type': 'def', 'symbol': 'comment_28'}
node_id: 29
(: applyGetNodeId (-> (Tree $a) ((Tree $a) NodeId NodeId Number) ((Tree $a) NodeId NodeId Number)))
{'type': 'type', 'symbol': 'applyGetNodeId'}
node_id: 30
;; Finds the NodeId of a subtree within the children of a target node.
{'type': 'def', 'symbol': 'comment_30'}
node_id: 31
;; Params:
{'type': 'def', 'symbol': 'comment_31'}
node_id: 32
;;   $tree: - The full tree to search.
{'type': 'def', 'symbol': 'comment_32'}
node_id: 33
;;   $targetId: - ID of the target node.
{'type': 'def', 'symbol': 'comment_33'}
node_id: 34
;;   $subtree: - The subtree to locate among the target node's children.
{'type': 'def', 'symbol': 'comment_34'}
node_id: 35
;;   $iter: - index to check children, increments recursively.
{'type': 'def', 'symbol': 'comment_35'}
node_id: 36
;; Returns:
{'type': 'def', 'symbol': 'comment_36'}
node_id: 37
;;   NodeId - The NodeId of the Subtree
{'type': 'def', 'symbol': 'comment_37'}
node_id: 38
(: getSubtreeId (-> (Tree $a) NodeId (Tree $a) Number NodeId))
{'type': 'type', 'symbol': 'getSubtreeId'}
node_id: 39
;; Retrieves the children list of a node identified by its NodeId.
{'type': 'def', 'symbol': 'comment_39'}
node_id: 40
;; Params:
{'type': 'def', 'symbol': 'comment_40'}
node_id: 41
;;   $tree: - The full tree to search.
{'type': 'def', 'symbol': 'comment_41'}
node_id: 42
;;   $id: - ID of the target node.
{'type': 'def', 'symbol': 'comment_42'}
node_id: 43
;; Returns:
{'type': 'def', 'symbol': 'comment_43'}
node_id: 44
;;   (List (Tree $a)) - The list of children of the target node.
{'type': 'def', 'symbol': 'comment_44'}
node_id: 45
(: getChildrenById (-> (Tree $a) NodeId (List (Tree $a))))
{'type': 'type', 'symbol': 'getChildrenById'}
node_id: 46
;; Creates a new tree with a node inserted above the given tree as its parent.
{'type': 'def', 'symbol': 'comment_46'}
node_id: 47
;; Params:
{'type': 'def', 'symbol': 'comment_47'}
node_id: 48
;;   $tree: - The original tree to be placed as a child.
{'type': 'def', 'symbol': 'comment_48'}
node_id: 49
;;   $node: - The new node to become the root, wrapping $tree.
{'type': 'def', 'symbol': 'comment_49'}
node_id: 50
;; Returns:
{'type': 'def', 'symbol': 'comment_50'}
node_id: 51
;;   (Tree $a) - A new mkTree with $node as the root and $tree as its only child.
{'type': 'def', 'symbol': 'comment_51'}
node_id: 52
(: insertAbove (-> (Tree $a) (Node $n) (Tree $a)))
{'type': 'type', 'symbol': 'insertAbove'}
node_id: 53
;; Replaces a subtree at a specific NodeId with a new subtree.
{'type': 'def', 'symbol': 'comment_53'}
node_id: 54
;; Params:
{'type': 'def', 'symbol': 'comment_54'}
node_id: 55
;;   $tree: - The tree to modify.
{'type': 'def', 'symbol': 'comment_55'}
node_id: 56
;;   $id: - ID of the node to be replace.
{'type': 'def', 'symbol': 'comment_56'}
node_id: 57
;;   $newSubtree: - The new subtree to insert.
{'type': 'def', 'symbol': 'comment_57'}
node_id: 58
;; Returns:
{'type': 'def', 'symbol': 'comment_58'}
node_id: 59
;;   (Tree $a) - The updated tree with $newSubtree at $id.
{'type': 'def', 'symbol': 'comment_59'}
node_id: 60
(: replaceNodeById (-> (Tree $a) NodeId (Tree $a) (Tree $a)))
{'type': 'type', 'symbol': 'replaceNodeById'}
node_id: 61
;; Appends a child to a target node's children and returns the updated tree and child's NodeId.
{'type': 'def', 'symbol': 'comment_61'}
node_id: 62
;; Parameters:
{'type': 'def', 'symbol': 'comment_62'}
node_id: 63
;;   $tree: - The tree to modify.
{'type': 'def', 'symbol': 'comment_63'}
node_id: 64
;;   $target: - ID of the target node
{'type': 'def', 'symbol': 'comment_64'}
node_id: 65
;;   $child: - The new child to append.
{'type': 'def', 'symbol': 'comment_65'}
node_id: 66
;; Returns:
{'type': 'def', 'symbol': 'comment_66'}
node_id: 67
;;   ((Tree $a) NodeId) - Tuple of updated tree and NodeId of the new child.
{'type': 'def', 'symbol': 'comment_67'}
node_id: 68
(: appendChild (-> (Tree $a) NodeId (Tree $a) ((Tree $a) NodeId)))
{'type': 'type', 'symbol': 'appendChild'}
node_id: 69
;; getChildrenByIdx -- retrieve children of a tree using index values
{'type': 'def', 'symbol': 'comment_69'}
node_id: 70
(: getChildrenByIdx (-> (Tree $a) Number (List (Tree $a))))
{'type': 'type', 'symbol': 'getChildrenByIdx'}
node_id: 71
;; check if tree is empty
{'type': 'def', 'symbol': 'comment_71'}
node_id: 72
(: isEmpty (-> (Tree $a) Bool))
{'type': 'type', 'symbol': 'isEmpty'}
node_id: 73
;; check if tree is null vertex 
{'type': 'def', 'symbol': 'comment_73'}
node_id: 74
(: isNullVertex (-> (Tree $a) Bool))
{'type': 'type', 'symbol': 'isNullVertex'}
node_id: 75
;; Takes a tree and decides if the node is an argument or not.
{'type': 'def', 'symbol': 'comment_75'}
node_id: 76
;; An argument is anything that's not an operator or a null vertex.
{'type': 'def', 'symbol': 'comment_76'}
node_id: 77
(: isArgument (-> (Tree $a) Bool))
{'type': 'type', 'symbol': 'isArgument'}
node_id: 78
;; A function to calculate the complexity of a tree.
{'type': 'def', 'symbol': 'comment_78'}
node_id: 79
;;  The complexity of a tree is the number of arguments it contains.
{'type': 'def', 'symbol': 'comment_79'}
node_id: 80
;;  That means, ANDs, ORs and NOTs have no complexity. 
{'type': 'def', 'symbol': 'comment_80'}
node_id: 81
;; Knobs, or null vetices aren't included in the complexity calculatio.
{'type': 'def', 'symbol': 'comment_81'}
node_id: 82
(: treeComplexity (-> (Tree $a) Number))
{'type': 'type', 'symbol': 'treeComplexity'}
node_id: 83
;; NOTE: for future use -- a function to determine the alphabet size of a given tree for computation of complexity ratio
{'type': 'def', 'symbol': 'comment_83'}
node_id: 84
;; takes a truth table and adds 3 (for AND,. OR and NOT) to the number of input labels
{'type': 'def', 'symbol': 'comment_84'}
node_id: 85
(: alphabetSize (-> (ITable $a) Number))
{'type': 'type', 'symbol': 'alphabetSize'}
node_id: 86
;; ===================
{'type': 'def', 'symbol': 'comment_86'}
node_id: 87
;; DEFINITIONS GROUPED
{'type': 'def', 'symbol': 'comment_87'}
node_id: 88
;; ===================
{'type': 'def', 'symbol': 'comment_88'}
node_id: 89
(= (getChildren (mkTree (mkNode $r) $children)) $children)
{'type': 'def', 'symbol': 'getChildren'}
node_id: 90
(= (getChildren (mkNullVex $children)) $children)
{'type': 'def', 'symbol': 'getChildren'}
node_id: 91
(= (getNodeValue (mkNullVex $xs)) (Error (mkNullVex $xs) "Null Vertex has no value"))
{'type': 'def', 'symbol': 'getNodeValue'}
node_id: 92
(= (updateChildren (mkTree (mkNode $r) $oldChildren) $newChildren)
   (mkTree (mkNode $r) $newChildren))
{'type': 'def', 'symbol': 'updateChildren'}
node_id: 93
(= (updateChildren (mkNullVex $oldChildren) $newChildren)
   (mkNullVex $newChildren))
{'type': 'def', 'symbol': 'updateChildren'}
node_id: 94
(= (preOrder (mkTree (mkNode $r) Nil)) $r)
{'type': 'def', 'symbol': 'preOrder'}
node_id: 95
(= (preOrder (mkNullVex $knobs)) ())
{'type': 'def', 'symbol': 'preOrder'}
node_id: 96
(= (preOrder (mkTree (mkNode $r) (Cons $x $xs)))
     (let*
         (
           ($lc  (List.map preOrder (Cons $x $xs)))
           ($lc' (List.filter (. not isUnit) $lc))
           ($lcE (List.listToExpr $lc'))
           ;; (()   (println! (Root: $r Children: $lc Children': $lc' Expression: $lcE)))
           ($exp (cons-atom $r $lcE))
         )
         $exp)
)
{'type': 'def', 'symbol': 'preOrder'}
node_id: 97
(= (buildTree $expr)
        (if (== (get-metatype $expr) Expression)
            (let ($head $tail) (decons-atom $expr)
                (mkTree (mkNode $head) (exprToList (map buildTree $tail))))
            (mkTree (mkNode $expr) Nil))
            )
{'type': 'def', 'symbol': 'buildTree'}
node_id: 98
(= (cleanTree $tree)
    (let*
        (
          ($preordered (preOrder $tree))
          ;; ($reduced (REDUCE $preordered))
        )
  (buildTree $preordered)))
{'type': 'def', 'symbol': 'cleanTree'}
node_id: 99
;; TODO: Remove when REDUCE is implemented.
{'type': 'def', 'symbol': 'comment_99'}
node_id: 100
;; NOTE: (buildTree $reduced) placeholder removed to avoid unmatched parens
{'type': 'def', 'symbol': 'comment_100'}
node_id: 101
(= (getNodeValue (mkTree $nodeValue $chl)) $nodeValue)
{'type': 'def', 'symbol': 'getNodeValue'}
node_id: 102
(= (getNodeId $tree $targetTree (mkNodeId $parentIdx))
    (if (== $tree $targetTree)
        (mkNodeId $parentIdx)
        (chain (getChildren $tree) $children
        (chain (List.index $children $targetTree) $targetIdx
        (if (== $targetIdx -1)
            (chain (List.foldl applyGetNodeId ($targetTree (mkNodeId $parentIdx) (mkNodeId (-1)) 1) $children) $state
              (let ($_ $__ $nodeId $iter) $state $nodeId))
            (if (== $parentIdx (0)) ;; If parentIdx is (0) don't include it in the index.
                (mkNodeId ((+ 1 $targetIdx)))
                (mkNodeId (unionAtom $parentIdx ((+ 1 $targetIdx))))))))))
{'type': 'def', 'symbol': 'getNodeId'}
node_id: 103
(= (applyGetNodeId $currTree ($targetTree (mkNodeId $parentIdx) $accId $iter))
    (if (== $accId (mkNodeId (-1)))
        (chain (getNodeId $currTree $targetTree (mkNodeId ($iter))) $nodeId
        (chain (if (== $parentIdx (0)) (mkNodeId $idx) (mkNodeId (unionAtom $parentIdx $idx))) $newId ;; If parentIdx (0) don't include it in the index.
          (let (mkNodeId $idx) $nodeId
            (if (== $idx (-1))
                ($targetTree (mkNodeId $parentIdx) $nodeId (+ 1 $iter))
                ($targetTree $nodeId $newId (+ 1 $iter))))))
        ($targetTree (mkNodeId $pareantIdx) $accId (+ 1 $iter))))
{'type': 'def', 'symbol': 'applyGetNodeId'}
node_id: 104
(= (getSubtreeId $tree (mkNodeId $targetId) $subtree $iter)
   (let*
     (
       ($targetNode (getNodeById $tree (mkNodeId $targetId)))
       ($children   (getChildren $targetNode))
       ($currNode   (List.getByIdx $children $iter))
     )
     (if (== $currNode $subtree)
         (let*
           (
             ($index (+ $iter 1))
             ($idOfSubtree (union-atom $targetId ($index)))
           )
           (mkNodeId $idOfSubtree))
         (getSubtreeId $tree (mkNodeId $targetId) $subtree (+ $iter 1)))))
{'type': 'def', 'symbol': 'getSubtreeId'}
node_id: 105
(= (getNodeId $tree $targetTree) (getNodeId $tree $targetTree (mkNodeId (0))))
{'type': 'def', 'symbol': 'getNodeId'}
node_id: 106
(= (getChildrenById $tree (mkNodeId $id))
   (let $targetNode (getNodeById $tree (mkNodeId $id))
     (getChildren $targetNode)))
{'type': 'def', 'symbol': 'getChildrenById'}
node_id: 107
(= (insertAbove $tree $node)
   (mkTree $node (Cons $tree Nil))
)
{'type': 'def', 'symbol': 'insertAbove'}
node_id: 108
(= (replaceNodeById $tree (mkNodeId $id) $newSubtree)

   ;; If no more id or targetTree is root.
   (if (or (== $id ()) (== (mkNodeId $id) (mkNodeId (0)))) ;; Without the mkNodeId constructor the interpreter treats the () and (0) as different types.
       $newSubtree
       (let* (($headId (car-atom $id))
              ($tailId (cdr-atom $id))
              ($children (getChildren $tree))
              ($childToUpdate (List.getByIdx $children (- $headId 1)) )
              ($updatedChild
                 (if (== $tailId ())
                     $newSubtree
                     (replaceNodeById $childToUpdate (mkNodeId $tailId) $newSubtree)))
              ($newChildren
                 (List.replaceAt $children (- $headId 1) $updatedChild)))
         
         (updateChildren $tree $newChildren))))
{'type': 'def', 'symbol': 'replaceNodeById'}
node_id: 109
(= (appendChild (mkNullVex Nil) $targetId $child) ($child (mkNodeId (0))))
{'type': 'def', 'symbol': 'appendChild'}
node_id: 110
(= (appendChild (mkNullVex (Cons $x $xs)) $targetId $child) (Error (mkNullVex (Cons $x $xs)) "Null vertex can't have more than one child"))
{'type': 'def', 'symbol': 'appendChild'}
node_id: 111
(= (appendChild (mkTree $node $children) (mkNodeId $target) $child)
   (let*
      (
        ( $tree (mkTree $node $children))
        ( $targetNode (getNodeById $tree (mkNodeId $target)))
        ( $childrenTgt (getChildren $targetNode))
        ( $updatedChildrenTgt (List.append $child $childrenTgt))
        ( $childIndex (List.length $updatedChildrenTgt))

        ;; Comparison has to be in mkNodeId constructor because if not,
        ;;    when the expression size is different so will the type and
        ;;    cause bad type error sometimes. For example, (2 3) 's type
        ;;    is (Number Number) and (0) 's type is (Number) hence the
        ;;    interpreter throws a bad type error.
        ( $idOfChild (if (== (mkNodeId $target) (mkNodeId (0))) ($childIndex) (union-atom $target ($childIndex))))
        ( $newTargetSubtree (updateChildren $targetNode $updatedChildrenTgt))
        ( $updatedTree (replaceNodeById $tree (mkNodeId $target) $newTargetSubtree))
      )
    ($updatedTree (mkNodeId $idOfChild))))
{'type': 'def', 'symbol': 'appendChild'}
node_id: 112
(= (getChildrenByIdx $tree $idx)
        (case $tree
            (((mkTree (mkNode $r) $childrenTgt) (List.getByIdx $childrenTgt $idx))
              ((mkNullVex $childrenTgt) (List.getByIdx $childrenTgt $idx))
              ($else (Error (Node not found or invalid))))))
{'type': 'def', 'symbol': 'getChildrenByIdx'}
node_id: 113
(= (isEmpty $tree)
    (case $tree
        (((mkNullVex Nil) True)
        ($else False))))
{'type': 'def', 'symbol': 'isEmpty'}
node_id: 114
(= (isNullVertex $tree)
    (case $tree
        (((mkNullVex $children) True)
         ($else False))))
{'type': 'def', 'symbol': 'isNullVertex'}
node_id: 115
(= (isArgument (mkNullVex $x)) False)
{'type': 'def', 'symbol': 'isArgument'}
node_id: 116
(= (isArgument (mkTree (mkNode $x) $children))
   (and (not (isMember $x (AND OR NOT))) (== $children Nil)))
{'type': 'def', 'symbol': 'isArgument'}
node_id: 117
(= (treeComplexity (mkNullVex $x)) 0)
{'type': 'def', 'symbol': 'treeComplexity'}
node_id: 118
(= (treeComplexity (mkTree (mkNode $a) $children)) ;; AND, OR and NOT have no complexity
   (if (isArgument (mkTree (mkNode $a) $children))
       1
       (List.sum (List.map treeComplexity $children))))
{'type': 'def', 'symbol': 'treeComplexity'}
node_id: 119
(= (alphabetSize (mkITable $rows $labels)) 
    (+ 3 (- (List.length $labels) 1)))
{'type': 'def', 'symbol': 'alphabetSize'}
node_id: 120
potential_chunks: [[1], [2], [3], [4], [5], [6], [7], [8], [9], [16], [17], [18], [19], [20], [21], [22], [23], [24], [104, 30], [27], [28], [29], [31], [32], [33], [34], [35], [36], [37], [38], [40], [41], [42], [43], [44], [45], [47], [48], [49], [50], [51], [52], [54], [55], [56], [57], [58], [59], [60], [62], [63], [64], [65], [66], [67], [68], [70], [72], [74], [107, 46], [95, 96, 97, 13], [93, 94, 12], [98, 14], [92, 102, 10], [105, 39], [103, 106, 25, 26], [108, 53], [110, 111, 112, 69], [113, 71], [114, 73], [115, 75], [76], [77], [79], [80], [81], [82], [84], [85], [87], [88], [89], [90, 91, 11], [99, 15], [100], [101], [109, 61], [116, 117, 78], [118, 119, 83], [120, 86]]
final_chunks: [';; =========================', ';; TYPE SIGNATURES GROUPED', ';; =========================', '(: Tree (-> $a Type))', '(: mkTree (-> (Node $a) (List (Tree $a)) (Tree $a)))', '(: Node (-> $a Type))', '(: mkNode (-> $a (Node $a)))', '(: NullVertex (Tree $a))', '(: mkNullVex (-> (List (Tree $a)) (Tree $a)))', ';; Get an id of a certain node. And (0) if the root node.', ';; Example:', ';;    Id of A in the (AND (OR (AND A B))) => (1 1 1)', ';;    Id of (AND A B) in the (AND (OR (AND A B))) => (1 1)', ';; Params:', ';;   $tree: The full tree to search', ';;   $targetTree: The target tree to find the ID of.', ';; Returns:', ';;   NodeId: The id of the targetTree if found.', "(= (applyGetNodeId $currTree ($targetTree (mkNodeId $parentIdx) $accId $iter))\n    (if (== $accId (mkNodeId (-1)))\n        (chain (getNodeId $currTree $targetTree (mkNodeId ($iter))) $nodeId\n        (chain (if (== $parentIdx (0)) (mkNodeId $idx) (mkNodeId (unionAtom $parentIdx $idx))) $newId ;; If parentIdx (0) don't include it in the index.\n          (let (mkNodeId $idx) $nodeId\n            (if (== $idx (-1))\n                ($targetTree (mkNodeId $parentIdx) $nodeId (+ 1 $iter))\n                ($targetTree $nodeId $newId (+ 1 $iter))))))\n        ($targetTree (mkNodeId $pareantIdx) $accId (+ 1 $iter))))\n(: applyGetNodeId (-> (Tree $a) ((Tree $a) NodeId NodeId Number) ((Tree $a) NodeId NodeId Number)))", ';; Helper function for the getNodeId function.', ";;   The function's sole purpose is to make the", ';;   getNodeById compatible for the foldr function call.', ';; Finds the NodeId of a subtree within the children of a target node.', ';; Params:', ';;   $tree: - The full tree to search.', ';;   $targetId: - ID of the target node.', ";;   $subtree: - The subtree to locate among the target node's children.", ';;   $iter: - index to check children, increments recursively.', ';; Returns:', ';;   NodeId - The NodeId of the Subtree', ';; Retrieves the children list of a node identified by its NodeId.', ';; Params:', ';;   $tree: - The full tree to search.', ';;   $id: - ID of the target node.', ';; Returns:', ';;   (List (Tree $a)) - The list of children of the target node.', ';; Creates a new tree with a node inserted above the given tree as its parent.', ';; Params:', ';;   $tree: - The original tree to be placed as a child.', ';;   $node: - The new node to become the root, wrapping $tree.', ';; Returns:', ';;   (Tree $a) - A new mkTree with $node as the root and $tree as its only child.', ';; Replaces a subtree at a specific NodeId with a new subtree.', ';; Params:', ';;   $tree: - The tree to modify.', ';;   $id: - ID of the node to be replace.', ';;   $newSubtree: - The new subtree to insert.', ';; Returns:', ';;   (Tree $a) - The updated tree with $newSubtree at $id.', ";; Appends a child to a target node's children and returns the updated tree and child's NodeId.", ';; Parameters:', ';;   $tree: - The tree to modify.', ';;   $target: - ID of the target node', ';;   $child: - The new child to append.', ';; Returns:', ';;   ((Tree $a) NodeId) - Tuple of updated tree and NodeId of the new child.', ';; getChildrenByIdx -- retrieve children of a tree using index values', ';; check if tree is empty', ';; check if tree is null vertex ', '(= (getChildrenById $tree (mkNodeId $id))\n   (let $targetNode (getNodeById $tree (mkNodeId $id))\n     (getChildren $targetNode)))\n(: getChildrenById (-> (Tree $a) NodeId (List (Tree $a))))', "(= (preOrder (mkTree (mkNode $r) Nil)) $r)\n(= (preOrder (mkNullVex $knobs)) ())\n(= (preOrder (mkTree (mkNode $r) (Cons $x $xs)))\n     (let*\n         (\n           ($lc  (List.map preOrder (Cons $x $xs)))\n           ($lc' (List.filter (. not isUnit) $lc))\n           ($lcE (List.listToExpr $lc'))\n           ;; (()   (println! (Root: $r Children: $lc Children': $lc' Expression: $lcE)))\n           ($exp (cons-atom $r $lcE))\n         )\n         $exp)\n)\n(: preOrder (-> (Tree $a) $a))", '(= (updateChildren (mkTree (mkNode $r) $oldChildren) $newChildren)\n   (mkTree (mkNode $r) $newChildren))\n(= (updateChildren (mkNullVex $oldChildren) $newChildren)\n   (mkNullVex $newChildren))\n(: updateChildren (-> (Tree $a) (List (Tree $a)) (Tree $a)))', '(= (buildTree $expr)\n        (if (== (get-metatype $expr) Expression)\n            (let ($head $tail) (decons-atom $expr)\n                (mkTree (mkNode $head) (exprToList (map buildTree $tail))))\n            (mkTree (mkNode $expr) Nil))\n            )\n(: buildTree (-> $a (Tree $a)))', '(= (getNodeValue (mkNullVex $xs)) (Error (mkNullVex $xs) "Null Vertex has no value"))\n(= (getNodeValue (mkTree $nodeValue $chl)) $nodeValue)\n(: getNodeValue (-> (Tree $a) (Node $a)))', '(= (getSubtreeId $tree (mkNodeId $targetId) $subtree $iter)\n   (let*\n     (\n       ($targetNode (getNodeById $tree (mkNodeId $targetId)))\n       ($children   (getChildren $targetNode))\n       ($currNode   (List.getByIdx $children $iter))\n     )\n     (if (== $currNode $subtree)\n         (let*\n           (\n             ($index (+ $iter 1))\n             ($idOfSubtree (union-atom $targetId ($index)))\n           )\n           (mkNodeId $idOfSubtree))\n         (getSubtreeId $tree (mkNodeId $targetId) $subtree (+ $iter 1)))))\n(: getSubtreeId (-> (Tree $a) NodeId (Tree $a) Number NodeId))', "(= (getNodeId $tree $targetTree (mkNodeId $parentIdx))\n    (if (== $tree $targetTree)\n        (mkNodeId $parentIdx)\n        (chain (getChildren $tree) $children\n        (chain (List.index $children $targetTree) $targetIdx\n        (if (== $targetIdx -1)\n            (chain (List.foldl applyGetNodeId ($targetTree (mkNodeId $parentIdx) (mkNodeId (-1)) 1) $children) $state\n              (let ($_ $__ $nodeId $iter) $state $nodeId))\n            (if (== $parentIdx (0)) ;; If parentIdx is (0) don't include it in the index.\n                (mkNodeId ((+ 1 $targetIdx)))\n                (mkNodeId (unionAtom $parentIdx ((+ 1 $targetIdx))))))))))\n(= (getNodeId $tree $targetTree) (getNodeId $tree $targetTree (mkNodeId (0))))\n(: getNodeId (-> (Tree $a) (Tree $a) NodeId))\n(: getNodeId (-> (Tree $a) (Tree $a) NodeId NodeId))", '(= (insertAbove $tree $node)\n   (mkTree $node (Cons $tree Nil))\n)\n(: insertAbove (-> (Tree $a) (Node $n) (Tree $a)))', '(= (appendChild (mkNullVex Nil) $targetId $child) ($child (mkNodeId (0))))\n(= (appendChild (mkNullVex (Cons $x $xs)) $targetId $child) (Error (mkNullVex (Cons $x $xs)) "Null vertex can\'t have more than one child"))', '(\n=\n(appendChild (mkTree $node $children) (mkNodeId $target) $child)', "(let*\n      (\n        ( $tree (mkTree $node $children))\n        ( $targetNode (getNodeById $tree (mkNodeId $target)))\n        ( $childrenTgt (getChildren $targetNode))\n        ( $updatedChildrenTgt (List.append $child $childrenTgt))\n        ( $childIndex (List.length $updatedChildrenTgt))\n\n        ;; Comparison has to be in mkNodeId constructor because if not,\n        ;;    when the expression size is different so will the type and\n        ;;    cause bad type error sometimes. For example, (2 3) 's type\n        ;;    is (Number Number) and (0) 's type is (Number) hence the\n        ;;    interpreter throws a bad type error.\n        ( $idOfChild (if (== (mkNodeId $target) (mkNodeId (0))) ($childIndex) (union-atom $target ($childIndex))))\n        ( $newTargetSubtree (updateChildren $targetNode $updatedChildrenTgt))\n        ( $updatedTree (replaceNodeById $tree (mkNodeId $target) $newTargetSubtree))\n      )\n    ($updatedTree (mkNodeId $idOfChild)))\n)", '(: appendChild (-> (Tree $a) NodeId (Tree $a) ((Tree $a) NodeId)))', '(= (getChildrenByIdx $tree $idx)\n        (case $tree\n            (((mkTree (mkNode $r) $childrenTgt) (List.getByIdx $childrenTgt $idx))\n              ((mkNullVex $childrenTgt) (List.getByIdx $childrenTgt $idx))\n              ($else (Error (Node not found or invalid))))))\n(: getChildrenByIdx (-> (Tree $a) Number (List (Tree $a))))', '(= (isEmpty $tree)\n    (case $tree\n        (((mkNullVex Nil) True)\n        ($else False))))\n(: isEmpty (-> (Tree $a) Bool))', '(= (isNullVertex $tree)\n    (case $tree\n        (((mkNullVex $children) True)\n         ($else False))))\n(: isNullVertex (-> (Tree $a) Bool))', ';; Takes a tree and decides if the node is an argument or not.', ";; An argument is anything that's not an operator or a null vertex.", ';; A function to calculate the complexity of a tree.', ';;  The complexity of a tree is the number of arguments it contains.', ';;  That means, ANDs, ORs and NOTs have no complexity. ', ";; Knobs, or null vetices aren't included in the complexity calculatio.", ';; NOTE: for future use -- a function to determine the alphabet size of a given tree for computation of complexity ratio', ';; takes a truth table and adds 3 (for AND,. OR and NOT) to the number of input labels', ';; ===================', ';; DEFINITIONS GROUPED', ';; ===================', '(= (getChildren (mkTree (mkNode $r) $children)) $children)\n(= (getChildren (mkNullVex $children)) $children)\n(: getChildren (-> (Tree $a) (List (Tree $a))))', '(= (cleanTree $tree)\n    (let*\n        (\n          ($preordered (preOrder $tree))\n          ;; ($reduced (REDUCE $preordered))\n        )\n  (buildTree $preordered)))\n(: cleanTree (-> (Tree $a) (Tree $a)))', ';; TODO: Remove when REDUCE is implemented.', ';; NOTE: (buildTree $reduced) placeholder removed to avoid unmatched parens', '(= (replaceNodeById $tree (mkNodeId $id) $newSubtree)\n\n   ;; If no more id or targetTree is root.\n   (if (or (== $id ()) (== (mkNodeId $id) (mkNodeId (0)))) ;; Without the mkNodeId constructor the interpreter treats the () and (0) as different types.\n       $newSubtree\n       (let* (($headId (car-atom $id))\n              ($tailId (cdr-atom $id))\n              ($children (getChildren $tree))\n              ($childToUpdate (List.getByIdx $children (- $headId 1)) )\n              ($updatedChild\n                 (if (== $tailId ())\n                     $newSubtree\n                     (replaceNodeById $childToUpdate (mkNodeId $tailId) $newSubtree)))\n              ($newChildren\n                 (List.replaceAt $children (- $headId 1) $updatedChild)))\n         \n         (updateChildren $tree $newChildren))))\n(: replaceNodeById (-> (Tree $a) NodeId (Tree $a) (Tree $a)))', '(= (isArgument (mkNullVex $x)) False)\n(= (isArgument (mkTree (mkNode $x) $children))\n   (and (not (isMember $x (AND OR NOT))) (== $children Nil)))\n(: isArgument (-> (Tree $a) Bool))', '(= (treeComplexity (mkNullVex $x)) 0)\n(= (treeComplexity (mkTree (mkNode $a) $children)) ;; AND, OR and NOT have no complexity\n   (if (isArgument (mkTree (mkNode $a) $children))\n       1\n       (List.sum (List.map treeComplexity $children))))\n(: treeComplexity (-> (Tree $a) Number))', '(= (alphabetSize (mkITable $rows $labels)) \n    (+ 3 (- (List.length $labels) 1)))\n(: alphabetSize (-> (ITable $a) Number))']
Chunks Stored in database
Chunking complete!
```