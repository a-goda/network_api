from netmiko import ConnectHandler

def send_command(command, host, username, password, device_type):

    node = ConnectHandler(host=host, username=username, password=password, device_type=device_type)

    response = node.send_command(command, use_genie=True)

    return response

# def send_show_command(command, **node):

#     node = ConnectHandler(host=node['host'], username=node['username'], password=node['password'], device_type=node['device_type'])

#     response = node.send_command(command, use_genie=True)

#     return response
