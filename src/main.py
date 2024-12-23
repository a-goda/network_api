# fastapi requirements
from typing import Union
from fastapi import FastAPI, Depends
from pydantic import BaseModel, SecretStr

# private code imports
from support_modules.ssh_pyats import send_command
from support_modules.netconf_client import netconf_get_capability, netconf_get_all_capabilities

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## SSH

- **SSH** a host and send get the output of show commands.
- **supported platforms**: \n

 _a10, accedian, adtran_os, adva_fsp150f2, adva_fsp150f3, alaxala_ax36s, alaxala_ax26s, alcatel_aos, alcatel_sros, 
 allied_telesis_awplus, apresia_aeos, arista_eos, arris_cer, aruba_os, aruba_aoscx, aruba_osswitch, aruba_procurve, audiocode_72, audiocode_66, 
 audiocode_shell, avaya_ers, avaya_vsp, broadcom_icos, brocade_fos, brocade_fastiron, brocade_netiron, brocade_nos, brocade_vdx, brocade_vyos, 
 checkpoint_gaia, calix_b6, casa_cmts, cdot_cros, centec_os, ciena_saos, cisco_asa, cisco_apic, cisco_ftd, cisco_ios, cisco_nxos, cisco_s200, 
 cisco_s300, cisco_tp, cisco_viptela, cisco_wlc, cisco_xe, cisco_xr, cloudgenix_ion, coriant, dell_dnos9, dell_force10, dell_os6, dell_os9, 
 dell_os10, dell_sonic, dell_powerconnect, dell_isilon, dlink_ds, digi_transport, endace, eltex, eltex_esr, enterasys, ericsson_ipos, 
 ericsson_mltn63, ericsson_mltn66, extreme, extreme_ers, extreme_exos, extreme_netiron, extreme_nos, extreme_slx, extreme_tierra, extreme_vdx, 
 extreme_vsp, extreme_wing, f5_ltm, f5_tmsh, f5_linux, fiberstore_fsos, flexvnf, fortinet, garderos_grs, generic, generic_termserver, 
 hillstone_stoneos, hp_comware, hp_procurve, huawei, huawei_smartax, huawei_olt, huawei_vrp, huawei_vrpv8, ipinfusion_ocnos, juniper, 
 juniper_junos, juniper_screenos, keymile, keymile_nos, linux, mikrotik_routeros, mikrotik_switchos, mellanox, mellanox_mlnxos, mrv_lx, 
 mrv_optiswitch, netapp_cdot, netgear_prosafe, netscaler, nokia_sros, nokia_srl, oneaccess_oneos, ovs_linux, paloalto_panos, pluribus, 
 quanta_mesh, rad_etx, raisecom_roap, ruckus_fastiron, ruijie_os, sixwind_os, sophos_sfos, supermicro_smis, teldat_cit, tplink_jetstream, 
 ubiquiti_edge, ubiquiti_edgerouter, ubiquiti_edgeswitch, ubiquiti_unifiswitch, vertiv_mph, vyatta_vyos, vyos, watchguard_fireware, 
 zte_zxros, yamaha, zyxel_os, maipu_

## NETCONF

Connect to a host using NETCONF protocol over SSH

* **IETF** Standard namespaces.
* **Cisco** Cisco IOS-XE specific namespaces.
"""

tags_metadata = [
    {
        "name": "SSH",
        "description": "SSH a host and get the output of show commands.",
    },
    {
        "name": "SSH-Cisco",
        "description": "SSH a cisco host and get the output of show commands.",
    },
    {
        "name": "NETCONF",
        "description": "Connect to a host using NETCONF protocol over SSH",
    },
    {
        "name": "NETCONF-IETF",
        "description": "NETCONF namespaces related to IETF",
    },
    {
        "name": "NETCONF-Cisco",
        "description": "NETCONF namespaces related to Cisco",
        # "externalDocs": {
        #     "description": "Items external docs",
        #     "url": "https://fastapi.tiangolo.com/",
        # },
    },
]

class User(BaseModel):
    username: str
    password: SecretStr


app = FastAPI(openapi_tags=tags_metadata, description=description)


@app.get("/",include_in_schema=False)
def read_root():
    return {"Network gathering API, please refere to docs section \"your-hostname-ip:port/docs\" for more information."}


# @app.get("/ssh/command/", tags=["SSH"])
# def send_a_command(host: str, device_type:str, command: str, user: User = Depends()):
#     """
#     Send show command to a device
    
#     \b
#     Parameters:
#     - **host** (string): host IP address
#     - **username** (string): user account with enough privalage to execute the command
#     - **password** (string): user password
#     - **command** (string): command to be sent to the host
#     """
#     return send_command(command=command, host=host, username=user.username, password=user.password.get_secret_value(), device_type=device_type)

@app.get("/ssh/command/", tags=["SSH"])
def send_a_command(host: str, username:str, password:str, device_type:str, command: str):
    """
    Send show command to a device
    
    \b
    Parameters:
    - **host** (string): host IP address
    - **username** (string): user account with enough privalage to execute the command
    - **password** (string): user password
    - **command** (string): command to be sent to the host
    """
    return send_command(command=command, host=host, username=username, password=password, device_type=device_type)


@app.get("/ssh/cisco/version/", tags=["SSH-Cisco"])
def send_show_command(host: str, username:str, password:str, device_type:str='cisco_ios'):
    return send_command(host=host, username=username, password=password, device_type=device_type, command='show version')


@app.get("/ssh/cisco/arp/", tags=["SSH-Cisco"])
def send_show_command(host: str, username:str, password:str, device_type:str='cisco_ios'):
    return send_command(host=host, username=username, password=password, device_type=device_type, command='show ip arp')

@app.get("/ssh/cisco/cdp-neighbors/", tags=["SSH-Cisco"])
def send_show_command(host: str, username:str, password:str, device_type:str='cisco_ios', details:bool='False'):
    return send_command(host=host, username=username, password=password, device_type=device_type, command='show cdp neighbors detail' if details else 'show cdp neighbors')

@app.get("/ssh/cisco/lldp-neighbors/", tags=["SSH-Cisco"])
def send_show_command(host: str, username:str, password:str, device_type:str='cisco_ios', details:bool='False'):
    return send_command(host=host, username=username, password=password, device_type=device_type, command='show lldp neighbors detail' if details else 'show lldp neighbors')


@app.get("/netconf/capabilities/", tags=["NETCONF"])
def get_netconf_all_capabilities(host: str, username:str, password:str, port=830):
    rpc_reply = netconf_get_all_capabilities(host=host, username=username, password=password, port=port, hostkey_verify=False)
    return rpc_reply

@app.get("/netconf/capability/", tags=["NETCONF"])
def get_netconf_capability(host: str, username:str, password:str, namespace:str, model:str, port=830):
    flag, rpc_reply = netconf_get_capability(host=host, username=username, password=password, namespace=namespace, model=model, port=port, hostkey_verify=False)
    return rpc_reply

@app.get("/netconf/cisco/cisco-xe/cdp-oper/", tags=["NETCONF-Cisco"])
def get_netconf_capability(host: str, username:str, password:str, port=830):
    flag, rpc_reply = netconf_get_capability(host=host, username=username, password=password, namespace='http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper', model='cdp-neighbor-details', port=port, hostkey_verify=False)
    return rpc_reply

@app.get("/netconf/cisco/cisco-xe/lldp-oper/", tags=["NETCONF-Cisco"])
def get_netconf_capability(host: str, username:str, password:str, port=830):
    flag, rpc_reply = netconf_get_capability(host=host, username=username, password=password, namespace='http://cisco.com/ns/yang/Cisco-IOS-XE-lldp-oper', model='lldp-entries', port=port, hostkey_verify=False)
    return rpc_reply

@app.get("/netconf/cisco/cisco-xe/interfaces-oper/", tags=["NETCONF-Cisco"])
def get_netconf_capability(host: str, username:str, password:str, port=830):
    flag, rpc_reply = netconf_get_capability(host=host, username=username, password=password, namespace='http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper', model='interfaces', port=port, hostkey_verify=False)
    return rpc_reply

@app.get("/netconf/cisco/cisco-xe/arp-oper/", tags=["NETCONF-Cisco"])
def get_netconf_capability(host: str, username:str, password:str, port=830):
    flag, rpc_reply = netconf_get_capability(host=host, username=username, password=password, namespace='http://cisco.com/ns/yang/Cisco-IOS-XE-arp-oper', model='arp-data', port=port, hostkey_verify=False)
    return rpc_reply


@app.get("/netconf/IETF/interfaces/", tags=["NETCONF-IETF"])
def get_netconf_capability(host: str, username:str, password:str, port=830):
    flag, rpc_reply = netconf_get_capability(host=host, username=username, password=password, namespace='urn:ietf:params:xml:ns:yang:ietf-interfaces', model='interfaces', port=port, hostkey_verify=False)
    return rpc_reply

@app.get("/netconf/IETF/interfaces-state/", tags=["NETCONF-IETF"])
def get_netconf_capability(host: str, username:str, password:str, port=830):
    flag, rpc_reply = netconf_get_capability(host=host, username=username, password=password, namespace='urn:ietf:params:xml:ns:yang:ietf-interfaces', model='interfaces-state', port=port, hostkey_verify=False)
    return rpc_reply

@app.get("/netconf/IETF/routing/", tags=["NETCONF-IETF"])
def get_netconf_capability(host: str, username:str, password:str, port=830):
    flag, rpc_reply = netconf_get_capability(host=host, username=username, password=password, namespace='urn:ietf:params:xml:ns:yang:ietf-routing', model='routing', port=port, hostkey_verify=False)
    return rpc_reply

@app.get("/netconf/IETF/routing-state/", tags=["NETCONF-IETF"])
def get_netconf_capability(host: str, username:str, password:str, port=830):
    flag, rpc_reply = netconf_get_capability(host=host, username=username, password=password, namespace='urn:ietf:params:xml:ns:yang:ietf-routing', model='routing-state', port=port, hostkey_verify=False)
    return rpc_reply



