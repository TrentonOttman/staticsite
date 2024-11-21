class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        html = ""
        for prop in self.props:
            html = html + " " + prop + "=" + '"' + self.props[prop] + '"'
        return html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Value Required!")
        if self.tag == None:
            return self.value
        html_props = HTMLNode.props_to_html(self)
        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self, html=""):
        current_node = self

        if type(current_node) == LeafNode:
            html += LeafNode.to_html(current_node)
            return html
        
        if type(current_node) == ParentNode:
            if current_node.tag == None:
                raise ValueError("Tag Required!")
            if current_node.children == None or current_node.children == [None] or len(current_node.children) == 0:
                raise ValueError("Children Required!")
            
            html_props = HTMLNode.props_to_html(current_node)
            html = f"{html}<{current_node.tag}{html_props}>"

        for node in current_node.children:
            html = ParentNode.to_html(node, html)
            if node == current_node.children[-1]:
                html += f"</{current_node.tag}>"

        return html
