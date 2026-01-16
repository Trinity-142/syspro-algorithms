import java.util.ArrayList;

public class Trie {

    private final Node root;
    private final ArrayList<Node> nodes;
    int version;

    public Trie(String[] patterns) {
        root = new Node();
        nodes = new ArrayList<>();
        nodes.add(root);
        for (String pattern : patterns) {
            add(pattern);
        }
        version = 0;
    }

    public void findPatterns(String text) {
        Node curr = root;
        for (int i = 0; i < text.length(); ++i) {
            curr = next(curr, text.charAt(i));
            curr.counter++;
            Node temp = curr;
            while (temp != root) {
                if (temp.terminal) {
                    int start = i - temp.pattern.length() + 1;
                    String pattern = temp.pattern;
                    System.out.printf("Pattern \"%s\" was found at index %d\n", pattern, start);
                }
                temp = suf(temp);
            }
        }
    }

    public void getPatternCounters() {
        propagateCounters();
        for (Node node : nodes) {
            if (node.terminal) {
                System.out.printf("Pattern \"%s\" occurs %d times\n", node.pattern, node.counter);
            }
        }
    }

    private void add(String pattern) {
        Node curr = root;
        for (char c : pattern.toCharArray()) {
            if (curr.go.containsKey(c)) {
                curr = curr.go.get(c);
            } else {
                Node child = new Node();
                nodes.add(child);
                child.fromParent = c;
                child.parent = curr;
                curr.go.put(c, child);
                curr = child;
            }
        }
        curr.terminal = true;
        curr.pattern = pattern;
    }

    public void addPattern(String pattern) {
        version++;
        add(pattern);
        resetCounters(root);
    }

    private Node suf(Node v) {
        checkVersions(v);
        if (v.suffLink == null) {
            if (v == root || v.parent == root) {
                v.suffLink = root;
            } else {
                v.suffLink = next(suf(v.parent), v.fromParent);
            }
        }
        return v.suffLink;
    }

    private Node next(Node v, char c) {
        checkVersions(v);
        if (v.go.containsKey(c)) {
            return v.go.get(c);
        }
        if (v.goCache.containsKey(c)) {
            return v.goCache.get(c);
        }

        if (v == root) {
            v.goCache.put(c, root);
        } else {
            v.goCache.put(c, next(suf(v), c));
        }
        return v.goCache.get(c);
    }

    private void checkVersions(Node v) {
        if (v.version != this.version) {
            v.goCache.clear();
            v.suffLink = null;
            v.version = this.version;
        }
    }

    private void resetCounters(Node u) {
        u.counter = 0;
        for (Node child : u.go.values()) {
            resetCounters(child);
        }
    }

    private void propagateCounters() {
        nodes.sort((a, b) -> Integer.compare(b.pattern.length(), a.pattern.length()));
        for (Node v : nodes) {
            if (v == root) {
                continue;
            }
            Node link = suf(v);
            if (link != root) {
                link.counter += v.counter;
            }
        }
    }
}
