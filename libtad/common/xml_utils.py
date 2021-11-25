from libtad.common.exceptions import ServerSideException, MalformedXMLException
import xml.etree.ElementTree as ET

class XmlUtils:
    @staticmethod
    def check_for_errors(result: str) -> None:
        node: ET.Element = ET.fromstring(result)

        if not node.get("version"):
            raise MalformedXMLException("Expected 'version' attribute in data node")

        error_node: ET.Element = node.find("error")
        if error_node is not None:
            XmlUtils.handle_error(error_node)

    @staticmethod
    def handle_error(error_node: ET.Element) -> None:
        error_msg: str = error_node.text if error_node is not None else "Unspecified error"
        raise ServerSideException(error_msg)
        
