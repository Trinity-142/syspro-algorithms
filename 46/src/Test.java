import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.Objects;

public class Test {

    public static void main(String[] args) {
        test1();
        test2();
        test3();
        test4();
        test5();
    }

    static String run(Trie t, String text) {
        PrintStream origOut = System.out;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream capture = new PrintStream(baos);
        System.setOut(capture);
        try {
            t.findPatterns(text);
        } finally {
            System.setOut(origOut);
        }
        return baos.toString();
    }

    static String runCounts(Trie t) {
        PrintStream origOut = System.out;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream capture = new PrintStream(baos);
        System.setOut(capture);
        try {
            t.getPatternCounters();
        } finally {
            System.setOut(origOut);
        }
        return baos.toString();
    }

    static void test1() {
        System.out.println("--- Test 1 ---");
        String[] patterns = {"buy now", "free money"};
        String text = "buy now !!! free money !!! cheap offer";

        Trie trie = new Trie(patterns);

        String before = run(trie, text);
        String expectedBefore = """
            Pattern "buy now" was found at index 0
            Pattern "free money" was found at index %d
            """.formatted(text.indexOf("free money"));
        assertEquals(Objects.equals(before, expectedBefore));

        trie.addPattern("cheap offer");

        String after = run(trie, text);
        String expectedAfter = """
            Pattern "buy now" was found at index 0
            Pattern "free money" was found at index %d
            Pattern "cheap offer" was found at index %d
            """.formatted(text.indexOf("free money"), text.indexOf("cheap offer"));
        assertEquals(Objects.equals(after, expectedAfter));

        String counts = runCounts(trie);
        String expectedCounts = """
            Pattern "cheap offer" occurs 1 times
            Pattern "free money" occurs 1 times
            Pattern "buy now" occurs 1 times
            """;
        assertEquals(counts.equals(expectedCounts));
    }

    static void test2() {
        System.out.println("--- Test 2 ---");
        String[] patterns = {"ab", "abc"};
        String text = "xxabcdyy";

        Trie trie = new Trie(patterns);

        String before = run(trie, text);
        String expectedBefore = """
            Pattern "ab" was found at index 2
            Pattern "abc" was found at index 2
            """;
        assertEquals(Objects.equals(before, expectedBefore));

        trie.addPattern("abcd");

        String after = run(trie, text);
        String expectedAfter = """
            Pattern "ab" was found at index 2
            Pattern "abc" was found at index 2
            Pattern "abcd" was found at index 2
            """;
        assertEquals(Objects.equals(after, expectedAfter));

        String counts = runCounts(trie);
        String expectedCounts = """
            Pattern "abcd" occurs 1 times
            Pattern "abc" occurs 1 times
            Pattern "ab" occurs 1 times
            """;
        assertEquals(counts.equals(expectedCounts));
    }

    static void test3() {
        System.out.println("--- Test 3 ---");
        String[] patterns = {"aa"};
        String text = "aaaaa";

        Trie trie = new Trie(patterns);

        String before = run(trie, text);
        String expectedBefore = """
            Pattern "aa" was found at index 0
            Pattern "aa" was found at index 1
            Pattern "aa" was found at index 2
            Pattern "aa" was found at index 3
            """;
        assertEquals(Objects.equals(before, expectedBefore));

        trie.addPattern("aaa");

        String after = run(trie, text);
        String expectedAfter = """
            Pattern "aa" was found at index 0
            Pattern "aaa" was found at index 0
            Pattern "aa" was found at index 1
            Pattern "aaa" was found at index 1
            Pattern "aa" was found at index 2
            Pattern "aaa" was found at index 2
            Pattern "aa" was found at index 3
            """;
        assertEquals(Objects.equals(after, expectedAfter));

        String counts = runCounts(trie);
        String expectedCounts = """
            Pattern "aaa" occurs 3 times
            Pattern "aa" occurs 4 times
            """;
        assertEquals(counts.equals(expectedCounts));
    }

    static void test4() {
        System.out.println("--- Test 4 ---");
        String[] patterns = {"hello"};
        String text = "aaaabbbbcccc";

        Trie trie = new Trie(patterns);

        String before = run(trie, text);
        String expectedBefore = "";
        assertEquals(Objects.equals(before, expectedBefore));

        trie.addPattern("bbb");

        String after = run(trie, text);
        String expectedAfter = """
            Pattern "bbb" was found at index 4
            Pattern "bbb" was found at index 5
            """;
        assertEquals(Objects.equals(after, expectedAfter));

        String counts = runCounts(trie);
        String expectedCounts = """
            Pattern "hello" occurs 0 times
            Pattern "bbb" occurs 2 times
            """;
        assertEquals(counts.equals(expectedCounts));
    }

    static void test5() {
        System.out.println("--- Test 5 ---");
        String[] patterns = {"a"};
        String text = "abcabcabc";

        Trie trie = new Trie(patterns);

        String before = run(trie, text);
        String expectedBefore = """
            Pattern "a" was found at index 0
            Pattern "a" was found at index 3
            Pattern "a" was found at index 6
            """;
        assertEquals(Objects.equals(before, expectedBefore));

        trie.addPattern("abc");
        trie.addPattern("bc");

        String after = run(trie, text);
        String expectedAfter = """
            Pattern "a" was found at index 0
            Pattern "abc" was found at index 0
            Pattern "bc" was found at index 1
            Pattern "a" was found at index 3
            Pattern "abc" was found at index 3
            Pattern "bc" was found at index 4
            Pattern "a" was found at index 6
            Pattern "abc" was found at index 6
            Pattern "bc" was found at index 7
            """;
        assertEquals(Objects.equals(after, expectedAfter));

        String counts = runCounts(trie);
        String expectedCounts = """
            Pattern "abc" occurs 3 times
            Pattern "bc" occurs 3 times
            Pattern "a" occurs 3 times
            """;
        assertEquals(counts.equals(expectedCounts));
    }

    private static void assertEquals(boolean condition) {
        if (condition) {
            System.out.println("PASSED");
        } else {
            System.err.println("FAILED");
        }
    }
}
