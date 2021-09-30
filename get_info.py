from pyVim.connect import *
from pyVim.task import WaitForTask
from pyVmomi import vim
import atexit
import time

#get all VMs
def GetVMs(content):
    
    vm_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine],True)
    obj = [vm for vm in vm_view.view]
    vm_view.Destroy()
    return obj

#get some need info from vm (not template)
def info_vm(host, user, pwd):
    global content, hosts, hostPgDict
    serviceInstance = SmartConnectNoSSL(host = host, user = user, pwd=pwd)
    atexit.register(Disconnect, serviceInstance)
    content = serviceInstance.RetrieveContent()
    vm_info=list()
    vms = GetVMs(content)
    for one_vm in vms:
        if one_vm.summary.config.template == False:
            params_vm = {}
            params_vm['name'] = one_vm.summary.config.name
            params_vm['os'] = one_vm.summary.config.guestFullName
            params_vm['power'] = one_vm.summary.runtime.powerState
            params_vm['cpu'] = one_vm.summary.config.numCpu
            params_vm['ram'] = one_vm.summary.config.memorySizeMB
            vm_info.append(params_vm)
    return vm_info

#get annotation of vm by name
def info_tmp_ann(host, user, pwd, name ):
    global content, hosts, hostPgDict
    serviceInstance = SmartConnectNoSSL(host = host, user = user, pwd=pwd)
    atexit.register(Disconnect, serviceInstance)
    content = serviceInstance.RetrieveContent()
    vm_info=list()
    vms = GetVMs(content)
    for one_vm in vms:
        if one_vm.summary.config.name == name:
            if one_vm.summary.config.template == True:
                return one_vm.summary.config.annotation

#get some need info from templates
def info_tmp(host, user, pwd):
    global content, hosts, hostPgDict
    serviceInstance = SmartConnectNoSSL(host = host, user = user, pwd=pwd)
    atexit.register(Disconnect, serviceInstance)
    content = serviceInstance.RetrieveContent()
    all_vm = []
    vms = GetVMs(content)
    for one_vm in vms:
    	if one_vm.summary.config.template == True:
            annotation['name'] = one_vm.summary.config.name
            annotation['os'] = one_vm.summary.config.guestFullName
            annotation['cpu'] = one_vm.summary.config.numCpu
            annotation['ram'] = one_vm.summary.config.memorySizeMB
            all_vm.append(annotation)
    return all_vm    

#checks whether the vmware tools is installed   
def info_tools(host, user, pwd, vm_name, c):

    content = c.content
    container_vms = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for vm in container_vms.view:
        if vm.name == vm_name:
            vm_need = vm
            tools_status = vm.guest.toolsStatus
    if (tools_status == 'toolsNotInstalled' or tools_status == 'toolsNotRunning'):
        return 'true' 
    else:
        return 'false'       

#get all virtual machine names
def info_vm_names(host, user, pwd):
    global content, hosts, hostPgDict
    serviceInstance = SmartConnectNoSSL(host = host, user = user, pwd=pwd)
    atexit.register(Disconnect, serviceInstance)
    content = serviceInstance.RetrieveContent()
    all_vm = []
    vms = GetVMs(content)
    for one_vm in vms:
        if one_vm.summary.config.template == False:

            all_vm.append(one_vm.summary.config.name)
    return all_vm    
