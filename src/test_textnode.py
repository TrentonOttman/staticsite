import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import *
from splitdelimeter import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_all(self):
        node = TextNode("This is a text node", TextType.BOLD, "correct")
        node2 = TextNode("This is a text node", TextType.BOLD, "correct")
        self.assertEqual(node, node2)
    
    def test_uneq_text(self):
        node = TextNode("This is NOT text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_uneq_texttype(self):
        node = TextNode("This is text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_uneq_url(self):
        node = TextNode("This is text node", TextType.BOLD, "right")
        node2 = TextNode("This is a text node", TextType.BOLD, "wrong")
        self.assertNotEqual(node, node2)

    def test_text_to_html_TEXT(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        expected_html = "This is a text node"
        html = LeafNode.to_html(html_node)
        self.assertEqual(expected_html, html)

    def test_text_to_html_BOLD(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        expected_html = "<b>This is a text node</b>"
        html = LeafNode.to_html(html_node)
        self.assertEqual(expected_html, html)

    def test_text_to_html_IMAGE(self):
        node = TextNode("This is a text node", TextType.IMAGE, "path/to/image.jpeg")
        html_node = text_node_to_html_node(node)
        expected_html = "<img src=\"path/to/image.jpeg\" alt=\"This is a text node\"></img>"
        html = LeafNode.to_html(html_node)
        self.assertEqual(expected_html, html)

    def test_text_to_html_wrong_type(self):
        node = TextNode("This is a text node", "fake")
        with self.assertRaises(Exception):
            node = text_node_to_html_node(node) 

    def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word and another **bold word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_new_nodes = "[TextNode(This is text with a , text, None), TextNode(bold, bold, None), TextNode( word and another , text, None), TextNode(bold word, bold, None)]"
        self.assertEqual(expected_new_nodes, str(new_nodes))
        
    def test_split_delimiter_italic(self):
        node = TextNode("This is text with an *italic* word and another *italic word*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_new_nodes = "[TextNode(This is text with an , text, None), TextNode(italic, italic, None), TextNode( word and another , text, None), TextNode(italic word, italic, None)]"
        self.assertEqual(expected_new_nodes, str(new_nodes))

    def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code` block and another `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_new_nodes = "[TextNode(This is text with a , text, None), TextNode(code, code, None), TextNode( block and another , text, None), TextNode(code block, code, None)]"
        self.assertEqual(expected_new_nodes, str(new_nodes))

    def test_split_delimiter_multiple(self):
        node_list = []
        node1 = TextNode("This is text with a **bold** word", TextType.TEXT)
        node_list.append(node1)
        node2 = TextNode("More **bold words** here", TextType.TEXT)
        node_list.append(node2)
        node3 = TextNode("**Bold words are cool**", TextType.TEXT)
        node_list.append(node3)
        new_nodes = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        expected_new_nodes = "[TextNode(This is text with a , text, None), TextNode(bold, bold, None), TextNode( word, text, None), TextNode(More , text, None), TextNode(bold words, bold, None), TextNode( here, text, None), TextNode(Bold words are cool, bold, None)]"
        self.assertEqual(expected_new_nodes, str(new_nodes))

    def test_split_delimiter_not_text_type(self):
        node = TextNode("This is text with a **bold** word and another **bold word**", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_new_nodes = "[TextNode(This is text with a **bold** word and another **bold word**, code, None)]"
        self.assertEqual(expected_new_nodes, str(new_nodes))

    def test_split_delimiter_invalid_syntax(self):
        node = TextNode("This is text with a **bold* word and another **bold word**", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD) 

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected_result = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(expected_result, result)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected_result = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(expected_result, result)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_new_nodes = "[TextNode(This is text with a link , text, None), TextNode(to boot dev, link, https://www.boot.dev), TextNode( and , text, None), TextNode(to youtube, link, https://www.youtube.com/@bootdotdev)]"
        self.assertEqual(expected_new_nodes, str(new_nodes))

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image ![boots](boots.jpeg) and a picture of ![pacman](pacman.png) pacman",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_new_nodes = "[TextNode(This is text with an image , text, None), TextNode(boots, image, boots.jpeg), TextNode( and a picture of , text, None), TextNode(pacman, image, pacman.png), TextNode( pacman, text, None)]"
        self.assertEqual(expected_new_nodes, str(new_nodes))

    def test_split_delimiter_multiple_image(self):
        node_list = []
        node1 = TextNode("This is a picture of a dolphin ![dolphin](dolphin.png)", TextType.TEXT)
        node_list.append(node1)
        node2 = TextNode("A tiger ![tiger](tiger.png) here", TextType.TEXT)
        node_list.append(node2)
        node3 = TextNode("![cat](cat.png)", TextType.TEXT)
        node_list.append(node3)
        new_nodes = split_nodes_image(node_list)
        expected_new_nodes = "[TextNode(This is a picture of a dolphin , text, None), TextNode(dolphin, image, dolphin.png), TextNode(A tiger , text, None), TextNode(tiger, image, tiger.png), TextNode( here, text, None), TextNode(cat, image, cat.png)]"
        self.assertEqual(expected_new_nodes, str(new_nodes))

    def test_split_delimiter_no_images(self):
        node = TextNode("This should not be touched!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_new_nodes = "[TextNode(This should not be touched!, text, None)]"
        self.assertEqual(expected_new_nodes, str(new_nodes))

    def test_text_to_textnodes_one_each(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        expected_textnodes = "[TextNode(This is , text, None), TextNode(text, bold, None), TextNode( with an , text, None), TextNode(italic, italic, None), TextNode( word and a , text, None), TextNode(code block, code, None), TextNode( and an , text, None), TextNode(obi wan image, image, https://i.imgur.com/fJRm4Vk.jpeg), TextNode( and a , text, None), TextNode(link, link, https://boot.dev)]"
        self.assertEqual(expected_textnodes, str(textnodes))

    def test_text_to_textnodes_all_bold(self):
        text = "**This is text that is completely bold and has no other formatting!**"
        textnodes = text_to_textnodes(text)
        expected_textnodes = "[TextNode(This is text that is completely bold and has no other formatting!, bold, None)]"
        self.assertEqual(expected_textnodes, str(textnodes))

    def test_text_to_textnodes_invalid_syntax(self):
        text = "This is text that has an *error!**"
        with self.assertRaises(Exception):
            textnodes = text_to_textnodes(text)

    def test_markdown_to_blocks_standard(self):
        text = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        blocks = markdown_to_blocks(text)
        expected_blocks = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        self.assertEqual(expected_blocks, blocks)

    def test_markdown_to_blocks_extra_newlines(self):
        text = "\n\n# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n\n"
        blocks = markdown_to_blocks(text)
        expected_blocks = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        self.assertEqual(expected_blocks, blocks)

    def test_markdown_to_blocks_whitespace(self):
        text = "  # This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.   \n\n  * This is the first list item in a list block\n* This is a list item\n* This is another list item  "
        blocks = markdown_to_blocks(text)
        expected_blocks = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        self.assertEqual(expected_blocks, blocks)

    def test_block_to_block_type_heading(self):
        block = "### This is a heading!"
        block_type = block_to_block_type(block)
        expected_block_type = "heading"
        self.assertEqual(expected_block_type, block_type)

    def test_block_to_block_type_code(self):
        block = "```Code\nBlock\nHere```"
        block_type = block_to_block_type(block)
        expected_block_type = "code"
        self.assertEqual(expected_block_type, block_type)

    def test_block_to_block_type_quote(self):
        block = "> I am\n> a\n>quote!"
        block_type = block_to_block_type(block)
        expected_block_type = "quote"
        self.assertEqual(expected_block_type, block_type)

    def test_block_to_block_type_unordered_list(self):
        block = "* Star\n* Or\n- Hyphen\n- Work!"
        block_type = block_to_block_type(block)
        expected_block_type = "unordered_list"
        self.assertEqual(expected_block_type, block_type)

    def test_block_to_block_type_ordered_list(self):
        block = "1. Numbers\n2. Must\n3. Go\n4. Up"
        block_type = block_to_block_type(block)
        expected_block_type = "ordered_list"
        self.assertEqual(expected_block_type, block_type)

    def test_block_to_block_type_paragraph(self):
        block = "Boring paragraph\nNothing to see here"
        block_type = block_to_block_type(block)
        expected_block_type = "paragraph"
        self.assertEqual(expected_block_type, block_type)

    def test_markdown_to_html_node_heading(self):
        markdown = "### Simple Heading"
        html_node = markdown_to_html_node(markdown)
        expected_html_node = "HTMLNode(div, None, [HTMLNode(h3, None, [HTMLNode(None, Simple Heading, None, None)], None)], None)"
        self.assertEqual(expected_html_node, str(html_node))
  
    def test_markdown_to_html_node_code(self):
        markdown = "```Code Block```"
        html_node = markdown_to_html_node(markdown)
        expected_html_node = "HTMLNode(div, None, [HTMLNode(pre, None, [HTMLNode(code, None, [HTMLNode(None, Code Block, None, None)], None)], None)], None)"
        self.assertEqual(expected_html_node, str(html_node))

    def test_markdown_to_html_node_quote(self):
        markdown = "> Quote\n> Here"
        html_node = markdown_to_html_node(markdown)
        expected_html_node = "HTMLNode(div, None, [HTMLNode(blockquote, None, [HTMLNode(None,  Quote\n Here, None, None)], None)], None)"
        self.assertEqual(expected_html_node, str(html_node))

    def test_markdown_to_html_node_unordered_list(self):
        markdown = "* Unordered\n* List\n* Here"
        html_node = markdown_to_html_node(markdown)
        expected_html_node = "HTMLNode(div, None, [HTMLNode(ul, None, [HTMLNode(li, None, [HTMLNode(None, Unordered, None, None)], None), HTMLNode(li, None, [HTMLNode(None, List, None, None)], None), HTMLNode(li, None, [HTMLNode(None, Here, None, None)], None)], None)], None)"
        self.assertEqual(expected_html_node, str(html_node))

    def test_markdown_to_html_node_ordered_list(self):
        markdown = "1. Ordered\n2. List"
        html_node = markdown_to_html_node(markdown)
        expected_html_node = "HTMLNode(div, None, [HTMLNode(ol, None, [HTMLNode(li, None, [HTMLNode(None, Ordered, None, None)], None), HTMLNode(li, None, [HTMLNode(None, List, None, None)], None)], None)], None)"
        self.assertEqual(expected_html_node, str(html_node))

    def test_markdown_to_html_node_all(self):
        markdown = "### This is example *markdown* for **me** to convert!\n\nSimple paragraph... *ITALICS*\n\n* Unordered\n* List\n\n[link](https://www.boot.dev/)\n\n![image](https://i.imgur.com/fJRm4Vk.jpeg)\n\n*italics*\n\n**bold**\n\n```Code Block```"
        html_node = markdown_to_html_node(markdown)
        expected_html_node = "HTMLNode(div, None, [HTMLNode(h3, None, [HTMLNode(None, This is example , None, None), HTMLNode(i, markdown, None, None), HTMLNode(None,  for , None, None), HTMLNode(b, me, None, None), HTMLNode(None,  to convert!, None, None)], None), HTMLNode(p, None, [HTMLNode(None, Simple paragraph... , None, None), HTMLNode(i, ITALICS, None, None)], None), HTMLNode(ul, None, [HTMLNode(li, None, [HTMLNode(None, Unordered, None, None)], None), HTMLNode(li, None, [HTMLNode(None, List, None, None)], None)], None), HTMLNode(p, None, [HTMLNode(a, link, None, {'href': 'https://www.boot.dev/'})], None), HTMLNode(p, None, [HTMLNode(img, , None, {'src': 'https://i.imgur.com/fJRm4Vk.jpeg', 'alt': 'image'})], None), HTMLNode(p, None, [HTMLNode(i, italics, None, None)], None), HTMLNode(p, None, [HTMLNode(b, bold, None, None)], None), HTMLNode(pre, None, [HTMLNode(code, None, [HTMLNode(None, Code Block, None, None)], None)], None)], None)"
        self.assertEqual(expected_html_node, str(html_node))

    def test_extract_title_correct(self):
        markdown = "# This is a correct header!"
        header = extract_title(markdown)
        expected_header = "This is a correct header!"
        self.assertEqual(expected_header, header)

    def test_extract_title_incorrect(self):
        markdown = "### This is an incorrect header!"
        with self.assertRaises(Exception):
            header = extract_title(markdown)

    def test_extract_title_extralines(self):
        markdown = "# This is a correct header!"
        header = extract_title(markdown)
        expected_header = "This is a correct header!"
        self.assertEqual(expected_header, header)

if __name__ == "__main__":
    unittest.main()