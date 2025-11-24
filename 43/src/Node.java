class Node {

    int alive;
    Node left, right;

    public Node(int alive) {
        this.alive = alive;
    }

    public Node(Node left, Node right) {
        this.left = left;
        this.right = right;
        this.alive = (left != null ? left.alive : 0) + (right != null ? right.alive : 0);
    }
}
