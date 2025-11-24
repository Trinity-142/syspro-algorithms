public class Test {

    public static void main(String[] args) {
        test1();
        test2();
        test3();
        test4();
        test5();
        test6();
    }

    static void test1() {
        int[] nums = {1, 3, 5};
        PersistentSegmentTree tree = new PersistentSegmentTree(nums);
        int result = tree.gte(0, 2, 4);
        assertEquals(result == 1);
    }

    static void test2() {
        int[] nums = {10, 20, 30, 40, 50};
        PersistentSegmentTree tree = new PersistentSegmentTree(nums);
        int result = tree.gte(1, 3, 25);
        assertEquals (result == 2);
    }

    static void test3() {
        int[] nums = {2, 4, 6, 8};
        PersistentSegmentTree tree = new PersistentSegmentTree(nums);
        int result = tree.gte(0, 3, 4);
        assertEquals (result == 3);
    }

    static void test4() {
        int[] nums = {1, 2, 3};
        PersistentSegmentTree tree = new PersistentSegmentTree(nums);
        int result = tree.gte(0, 2, 10);
        assertEquals (result == 0);
    }

    static void test5() {
        int[] nums = {5, 5, 5};
        PersistentSegmentTree tree = new PersistentSegmentTree(nums);
        int result = tree.gte(0, 2, 1);
        assertEquals(result == 3);
    }

    static void test6() {
        int[] nums = {42};
        PersistentSegmentTree tree = new PersistentSegmentTree(nums);
        assertEquals(tree.gte(0, 0, 42) == 1);
        assertEquals(tree.gte(0, 0, 43) == 0);
    }

    private static void assertEquals(boolean condition) {
        if (condition) {
            System.out.println("PASSED");
        } else {
            System.err.println("FAILED");
        }
    }
}