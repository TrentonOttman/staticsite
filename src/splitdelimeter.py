from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        current_node_format = []
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = node.text.count(delimiter)
        if matches % 2 != 0:
            raise Exception("Invalid Markdown Syntax")

        for i in range(matches+1):
            node_text_list = node.text.split(delimiter, i+1)
            if node_text_list[i] == "":
                continue
            if i % 2 == 0:
                current_node_format.append(TextNode(node_text_list[i], TextType.TEXT))
            else:
                current_node_format.append(TextNode(node_text_list[i], text_type))
        new_nodes.extend(current_node_format)
    return new_nodes

def extract_markdown_images(text):
    # alt_text_matches = re.findall(r"!\[(.*?)\]", text)
    # link_matches = re.findall(r"\((.*?)\)", text)
    # zipped = zip(alt_text_matches, link_matches)
    # return list(zipped)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    # alt_text_matches = re.findall(r"\[(.*?)\]", text)
    # link_matches = re.findall(r"\((.*?)\)", text)
    # zipped = zip(alt_text_matches, link_matches)
    # return list(zipped)
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_node_format = []
        matches = extract_markdown_images(node.text)
        matches_count = len(matches)
        if matches_count == 0:
            new_nodes.append(node)
            continue

        for i in range(matches_count):
            node_text_list = node.text.split(f"![{matches[i][0]}]({matches[i][1]})", 1)
            if node_text_list[0] != "":
                current_node_format.append(TextNode(node_text_list[0], TextType.TEXT))
            current_node_format.append(TextNode(matches[i][0], TextType.IMAGE, matches[i][1]))
            preceding = node_text_list[0]
            node.text = node.text.replace(preceding, "", 1)
            node.text = node.text.replace(f"![{matches[i][0]}]({matches[i][1]})", "", 1)
            if i + 1 == matches_count and node.text != "":
                current_node_format.append(TextNode(node.text, TextType.TEXT))
        new_nodes.extend(current_node_format)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_node_format = []
        matches = extract_markdown_links(node.text)
        matches_count = len(matches)
        if matches_count == 0:
            new_nodes.append(node)
            continue

        for i in range(matches_count):
            node_text_list = node.text.split(f"[{matches[i][0]}]({matches[i][1]})", 1)
            if node_text_list[0] != "":
                current_node_format.append(TextNode(node_text_list[0], TextType.TEXT))
            current_node_format.append(TextNode(matches[i][0], TextType.LINK, matches[i][1]))
            preceding = node_text_list[0]
            node.text = node.text.replace(preceding, "", 1)
            node.text = node.text.replace(f"[{matches[i][0]}]({matches[i][1]})", "", 1)
            if i + 1 == matches_count and node.text != "":
                current_node_format.append(TextNode(node.text, TextType.TEXT))
        new_nodes.extend(current_node_format)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodelist = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodelist = split_nodes_delimiter(nodelist, "*", TextType.ITALIC)
    nodelist = split_nodes_delimiter(nodelist, "`", TextType.CODE)
    nodelist = split_nodes_image(nodelist)
    nodelist = split_nodes_link(nodelist)
    return nodelist

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = list(filter(lambda block: block != "", blocks))
    stripped_blocks = list(map(lambda block: block.strip(), filtered_blocks))
    return stripped_blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6}\ \w", block) != None:
        return "heading"
    if re.match(r"^`{3}(.*?)`{3}$", block, re.DOTALL) != None:
        return "code"
    lines = block.split("\n")
    for line in lines:
        if len(line) == 0:
            print("here")
            return "paragraph"
    correct_first_char_quote = True
    for line in lines:
        if line[0] != '>':
            correct_first_char_quote = False
    if correct_first_char_quote:
        return "quote"
    for line in lines:
        if len(line) < 3:
            print("here")
            return "paragraph"
    correct_first_char_unordered = True
    for line in lines:
        if (line[0] != '*' and line[0] != '-') or line[1] != " ":
            correct_first_char_unordered = False
    if correct_first_char_unordered:
        return "unordered_list"
    correct_first_char_ordered = True
    i = 1
    for line in lines:
        if line[0] != str(i) or line[1] != "." or line[2] != " ":
            correct_first_char_ordered = False
        i += 1
    if correct_first_char_ordered:
        return "ordered_list"
    return "paragraph"

def heading_to_tag_and_text(heading):
    if re.match(r"^#{6}", heading) != None:
        return "h6", heading[7:]
    if re.match(r"^#{5}", heading) != None:
        return "h5", heading[6:]
    if re.match(r"^#{4}", heading) != None:
        return "h4", heading[5:]
    if re.match(r"^#{3}", heading) != None:
        return "h3", heading[4:]
    if re.match(r"^#{2}", heading) != None:
        return "h2", heading[3:]
    return "h1", heading[2:]

def code_to_text(code):
    split_code = list(code)
    if split_code[3] == '\n':
        new_code = split_code[4:-3]
    else:
        new_code = split_code[3:-3]
    code_text = "".join(new_code)
    return code_text

def quote_to_text(quote):
    lines = quote.split("\n")
    new_lines = []
    for line in lines:
        new_line = line[2:]
        new_lines.append(new_line)
    text = "\n".join(new_lines)
    return text

def unordered_list_to_list_items(unordered_list):
    lines = unordered_list.split("\n")
    new_lines = []
    for line in lines:
        new_line = line[2:]
        children = text_to_children(new_line)
        ListItem = ParentNode("li", children)
        new_lines.append(ListItem)
    return new_lines

def ordered_list_to_list_items(ordered_list):
    lines = ordered_list.split("\n")
    new_lines = []
    for line in lines:
        new_line = line[3:]
        children = text_to_children(new_line)
        ListItem = ParentNode("li", children)
        new_lines.append(ListItem)
    return new_lines

def text_to_children(text):
    children_nodes = []
    node_list = text_to_textnodes(text)
    for node in node_list:
        children_nodes.append(text_node_to_html_node(node))
    return children_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_list = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            tag, text = heading_to_tag_and_text(block)
            children = text_to_children(text)
            BlockNode = ParentNode(tag, children)
        elif block_type == "code":
            text = code_to_text(block)
            children = text_to_children(text)
            CodeNode = ParentNode("code", children)
            BlockNode = ParentNode("pre", [CodeNode])
        elif block_type == "quote":
            text = quote_to_text(block)
            children = text_to_children(text)
            BlockNode = ParentNode("blockquote", children)
        elif block_type == "unordered_list":
            list_items = unordered_list_to_list_items(block)
            BlockNode = ParentNode("ul", list_items)
        elif block_type == "ordered_list":
            list_items = ordered_list_to_list_items(block)
            BlockNode = ParentNode("ol", list_items)
        else:
            children = text_to_children(block)
            BlockNode = ParentNode("p", children)
        blocks_list.append(BlockNode)
    FinalNode = ParentNode("div", blocks_list)
    return FinalNode

def extract_title(markdown):
    split_markdown = markdown.split("\n")
    for markdown in split_markdown:
        if re.match(r"^#\ ", markdown) != None:
            header = markdown[2:]
            stripped_header = header.strip()
            return stripped_header
    raise Exception("Not found!")
