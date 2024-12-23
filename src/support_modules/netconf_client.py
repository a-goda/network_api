from ncclient import manager
from ncclient.operations import RPCError
# import xml.dom.minidom
import re
import xmltodict
# import time
# import json
# import argparse

class NetconfClient:
    def __init__(self, host, username, password, port=830, hostkey_verify=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.hostkey_verify = hostkey_verify
        self.errors = []
        self.connected = False
        
    def connect(self):
        """
        Connect to a router using netconf over SSH, the default netconf port is 830
        """
        try:
            self.m = manager.connect(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                hostkey_verify=self.hostkey_verify
            )
            flag, capabilities = self.get_capabilities()
            if flag == 0: 
                # error getting capabilities
                return False
                
            
            self.capabilities = capabilities
            self.connected = True
            return True

        except Exception as e:
            return False                
        

    def close(self):
        self.m.close_session()

    def get_capabilities(self):
        capabilities = []
        try:
            for capability in self.m.server_capabilities:
                match = re.search(r'(.+)[?]module=(.*)', capability)
                if match:
                    capabilities.append((match.group(1), match.group(2)))
            
        except RPCError as e:
            # print(f"RPC Error: {str(e)}")
            return 0, None

        return 1, capabilities

    def is_capability_supported(self, capability):
        for cap in self.capabilities:                
            if capability in cap[0]:
                return True
        return False
    
    # def extract_data_from_xml(self, xml_data, model):
    #     dom = xml.dom.minidom.parseString(xml_data)
    #     print(dom)
    #     rpc_reply = dom.getElementsByTagName(model)
        
    #     if not rpc_reply:
    #         return -3
    #     return rpc_reply[0].toprettyxml()
    
    def get_model_data_by_namespace(self, model, namespace):
        if self.is_capability_supported(namespace):
            try:
                filter_str = f'<{model} xmlns="{namespace}"/>'
                data = self.m.get(filter=('subtree', filter_str)).data_xml
                # return self.extract_data_from_xml(data, model)
                return data
            except RPCError as e:
                print(f"RPC Error: {str(e)}")
                self.errors.append([model, namespace, str(e)])
                return -2
        else:
            return -1

def netconf_get_capability(host, username, password, model, namespace, port, hostkey_verify=False):
    
    # Instantiate the NetconfClient object
    router = NetconfClient(host=host, username=username, password=password, port=port, hostkey_verify=hostkey_verify)
        
    if router.connect():
        
        rpc_reply = router.get_model_data_by_namespace(model, namespace)
        router.close()

        if rpc_reply == -1:
            return -1, f'Connection established but not supported capability.'
        elif rpc_reply == -2:
            return -2, f'Connection established but failed to get model data.'
        elif rpc_reply == -3:
            return -3, f'Connection established but the model data is empty.'
        else:
            # return True, json.dumps(xmltodict.parse(rpc_reply), indent=4)
            return True, xmltodict.parse(rpc_reply)

    else:
        return 0, f'Connection error: failed to connect to the host {host}.'


def netconf_get_all_capabilities(host, username, password, port=830, hostkey_verify=False):
    
    # Instantiate the NetconfClient object
    router = NetconfClient(host=host, username=username, password=password, port=port, hostkey_verify=hostkey_verify)
        
    if router.connect():
        return router.capabilities
        

# if __name__ == "__main__":
    
    
    # command_namespaces_model = {
    #     'cdp neighbors':        ['http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper', 'cdp-neighbor-details'],
    #     'lldp neighbors':       ['http://cisco.com/ns/yang/Cisco-IOS-XE-lldp-oper', 'lldp-entries'],
    #     'interfaces Cisco':     ['http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper', 'interfaces'],
    #     'sh ip interface brief':['urn:ietf:params:xml:ns:yang:ietf-interfaces', 'interfaces'],
    #     'sh int brief':         ['urn:ietf:params:xml:ns:yang:ietf-interfaces', 'interfaces-state'],
    #     'sh ip arp':            ['http://cisco.com/ns/yang/Cisco-IOS-XE-arp-oper', 'arp-data'],
    #     'sh ip route':          ["urn:ietf:params:xml:ns:yang:ietf-routing", 'routing-state'],
    #     'sh vrf':               ["urn:ietf:params:xml:ns:yang:ietf-routing", 'routing']
    # }
    #  for k, cap in command_namespaces_model.items():
    #     flag, rpc_reply = netconf_client_connect(host="192.168.200.122", username="agoda", password="cisco", namespace=cap[0], model=cap[1], 
    #                                        connection_attempts=3, sleep_time=1, port=830, hostkey_verify=False, print_log=True)
    #     if flag is True:
    #             with open(f"./selected-models-data/{k}.xml", "w") as f:
    #                 f.write(rpc_reply)
    #             with open(f"./selected-models-data/{k}.json", "w") as f:
    #                 json.dump(xmltodict.parse(rpc_reply), f, indent=4)
    
    
    # parser = argparse.ArgumentParser(description='Netconf')

    # parser.add_argument("--host", type=str)
    # parser.add_argument("--username", type=str)
    # parser.add_argument("--password", type=str)
    # parser.add_argument("--namespace", type=str)
    # parser.add_argument("--model", type=str)
    # parser.add_argument("--attempts", type=int, default=3)
    # parser.add_argument("--sleep", type=int, default=1)
    # parser.add_argument("--port", type=int, default=830)
    # parser.add_argument("--output", type=str, default="xml")
    # parser.add_argument("--verify_hostkey", action='store_true') #verify host keys
    # parser.add_argument("--verbos", action='store_true') 
    # parser.add_argument("--save", action='store_true')
    # parser.add_argument("--path", type=str, default="./")

    # args = parser.parse_args()

    # host = args.host
    # username = args.username
    # password = args.password
    # namespace = args.namespace
    # model = args.model
    # connection_attempts = args.attempts
    # sleep_time = args.sleep
    # port = args.port
    # output = args.output
    # if output is not None:
    #     output = str(output).lower()
    # verbos = args.verbos
    # verify_hostkey = args.verify_hostkey
    # save = args.save
    # file_path = args.path

    # flag, rpc_reply = netconf_client_connect(host=host, username=username, password=password, namespace=namespace, model=model, connection_attempts=connection_attempts, 
    #                                          sleep_time=sleep_time, port=port, hostkey_verify=verify_hostkey, verbos=verbos, output=output)
    # # if flag is True:
    # if verbos: print(rpc_reply)

    # if save and flag > 0:   #if save and router is connected      
    #     if output == 'xml':
    #         with open(file_path, "w") as f:
    #             f.write(rpc_reply)
    #     if output == 'json':
    #         with open(file_path, "w") as f:
    #             json.dump(xmltodict.parse(rpc_reply), f, indent=4)
   


    
# netconf-client.py --verify_hostkey --verbos --host 192.168.200.122 --username agoda --password cisco --namespace http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper --model cdp-neighbor-details --sleep 0 --save --path ./selected-models-data/cdp-neighbor-details.json --output json 
    