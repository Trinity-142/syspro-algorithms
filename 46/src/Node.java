import java.util.HashMap;
import java.util.Map;

public class Node {

    boolean terminal;
    Map<Character, Node> go;
    Map<Character, Node> goCache;
    Node suffLink;
    Node parent;
    char fromParent;
    int version;
    String pattern;
    int counter;

    public Node() {
        pattern = "";
        terminal = false;
        go = new HashMap<>();
        goCache = new HashMap<>();
        version = 0;
        counter = 0;
    }
}
