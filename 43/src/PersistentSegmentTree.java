import static java.lang.Math.max;
import static java.lang.Math.min;

import java.util.Arrays;

class PersistentSegmentTree {

    Node[] roots;
    int[] nums;
    Integer[] idx;
    int n;

    public PersistentSegmentTree(int[] inputNums) {
        this.nums = inputNums;
        this.n = nums.length;
        this.idx = new Integer[n];
        for (int i = 0; i < n; i++) {
            idx[i] = i;
        }
        Arrays.sort(idx, (a, b) -> Integer.compare(nums[b], nums[a]));

        roots = new Node[n + 1];
        roots[0] = build(new Node(0), 0, n - 1);

        for (int i = 0; i < n; i++) {
            int originalPos = idx[i];
            roots[i + 1] = revive(roots[i], 0, n - 1, originalPos);
        }
    }

    private Node build(Node node, int vl, int vr) {
        if (vl == vr) {
            return new Node(0);
        }
        int m = (vl + vr) / 2;
        node.left = build(new Node(0), vl, m);
        node.right = build(new Node(0), m + 1, vr);
        return node;
    }

    private Node revive(Node root, int l, int r, int index) {
        Node copy = new Node(root.left, root.right);
        copy.alive = root.alive;
        copy.alive += 1;
        if (l == r) {
            return copy;
        }
        int m = (l + r) / 2;
        if (index <= m) {
            copy.left = revive(root.left, l, m, index);
            copy.right = root.right;
        } else {
            copy.left = root.left;
            copy.right = revive(root.right, m + 1, r, index);
        }
        return copy;
    }

    private int binarySearch(int[] array, int value) {
        int l = 0;
        int r = array.length;
        while (l < r) {
            int m = l + (r - l) / 2;
            if (array[m] < value) {
                l = m + 1;
            } else {
                r = m;
            }

        }
        return l;
    }

    private int _gte(Node root, int vl, int vr, int l, int r) {
        if (l == vl && r == vr) {
            return root.alive;
        }

        int m = (vr + vl) / 2;
        int res = 0;
        if (l <= m) {
            res += _gte(root.left, vl, m, l, min(r, m));
        }
        if (r > m) {
            res += _gte(root.right, m + 1, vr, max(l, m + 1), r);
        }
        return res;
    }

    public int gte(int l, int r, int k) {
        int index = binarySearch(nums, k);
        if (index >= n) { return 0; }
        Node root = roots[n - index];
        return _gte(root, 0, n - 1, l, r);
    }
}