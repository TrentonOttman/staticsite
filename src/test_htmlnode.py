import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "paragraph text", ["node1", "node2"], {"href": "https://www.google.com"})
        expected_html = " href=\"https://www.google.com\""
        html = HTMLNode.props_to_html(node)
        self.assertEqual(expected_html, html)

    def test_props_to_html_multiple(self):
        node = HTMLNode("li", "stuff goes here", ["node1", "node2"], {"href": "https://www.google.com", "target": "_blank",})
        expected_html = " href=\"https://www.google.com\" target=\"_blank\""
        html = HTMLNode.props_to_html(node)
        self.assertEqual(expected_html, html)

    def test_props_to_html_none(self):
        node = HTMLNode("li", "stuff goes here", ["node1", "node2"])
        expected_html = ""
        html = HTMLNode.props_to_html(node)
        self.assertEqual(expected_html, html)

    def test_leaf_to_html_no_props(self):
        node = LeafNode("p", "paragraph text")
        expected_html = "<p>paragraph text</p>"
        html = LeafNode.to_html(node)
        self.assertEqual(expected_html, html)

    def test_leaf_to_html_one_prop(self):
        node = LeafNode("p", "paragraph text", {"href": "https://www.google.com"})
        expected_html = "<p href=\"https://www.google.com\">paragraph text</p>"
        html = LeafNode.to_html(node)
        self.assertEqual(expected_html, html)

    def test_leaf_to_html_two_props(self):
        node = LeafNode("p", "paragraph text", {"href": "https://www.google.com", "target": "_blank",})
        expected_html = "<p href=\"https://www.google.com\" target=\"_blank\">paragraph text</p>"
        html = LeafNode.to_html(node)
        self.assertEqual(expected_html, html)

    def test_leaf_to_html_none_value(self):
        node = LeafNode("p", None, {"href": "https://www.google.com", "target": "_blank",})
        with self.assertRaises(ValueError):
            LeafNode.to_html(node)

    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        html = ParentNode.to_html(node)
        self.assertEqual(expected_html, html)

    def test_parent_to_html_property(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href": "https://www.google.com"}
        )
        expected_html = "<p href=\"https://www.google.com\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        html = ParentNode.to_html(node)
        self.assertEqual(expected_html, html)

    def test_parent_to_html_nested(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "c",
                    [
                        LeafNode("b", "More bold text"),
                        LeafNode(None, "Normal text"),
                    ],
                    {"target": "_blank"}
                ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href": "https://www.google.com"}
        )
        expected_html = "<p href=\"https://www.google.com\"><b>Bold text</b><c target=\"_blank\"><b>More bold text</b>Normal text</c><i>italic text</i>Normal text</p>"
        html = ParentNode.to_html(node)
        self.assertEqual(expected_html, html)

    def test_parent_to_html_doubly_nested(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "c",
                    [
                        LeafNode("b", "More bold text"),
                        ParentNode(
                            "d",
                            [
                                LeafNode("w", "super inner", {"depth": "pretty deep"})
                            ],
                        ),
                    ],
                    {"target": "_blank"}
                ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href": "https://www.google.com"}
        )
        expected_html = "<p href=\"https://www.google.com\"><b>Bold text</b><c target=\"_blank\"><b>More bold text</b><d><w depth=\"pretty deep\">super inner</w></d></c><i>italic text</i>Normal text</p>"
        html = ParentNode.to_html(node)
        self.assertEqual(expected_html, html)

    def test_parent_to_html_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href": "https://www.google.com"}
        )
        with self.assertRaises(ValueError):
            ParentNode.to_html(node)

    def test_parent_to_html_no_children(self):
        node = ParentNode(
            "p",
            [
            ],
            {"href": "https://www.google.com"}
        )
        with self.assertRaises(ValueError):
            ParentNode.to_html(node)

    def test_parent_to_html_deep_no_tag(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    None,
                    [
                        LeafNode("b", "More bold text"),
                        LeafNode(None, "Normal text"),
                    ],
                    {"target": "_blank"}
                ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href": "https://www.google.com"}
        )
        with self.assertRaises(ValueError):
            ParentNode.to_html(node)

    def test_parent_to_html_deep_no_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "q",
                    [
                    ],
                    {"target": "_blank"}
                ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href": "https://www.google.com"}
        )
        with self.assertRaises(ValueError):
            ParentNode.to_html(node)

if __name__ == "__main__":
    unittest.main()