from pyVim.connect import SmartConnectNoSSL
from pyVim.task import WaitForTask
from pyVmomi import vim
import atexit

def GetVMs(content):
    """
    getting all vms
    """
    vm_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    obj = [vm for vm in vm_view.view]
    vm_view.Destroy()
    return obj

#write annotation to template (if you want to write annotation to vm, change TRUE below)
def write_info(host, user, pwd, annotation, tmp):
    """
    write annotation to template
    (if you want to write annotation to vm, change TRUE below)
    :param host - host ip
    :param user - esxi host user
    :param pwd - esxi host password
    :param annotation: comment to VM
    :param tmp: vm`s name
    :return:
    """
    global content, hosts, hostPgDict
    serviceInstance = SmartConnectNoSSL(host = host, user = user, pwd=pwd)
    atexit.register(Disconnect, serviceInstance)
    content = serviceInstance.RetrieveContent()
    vms = GetVMs(content)
    for one_vm in vms:
        #here change TRUE
        if one_vm.summary.config.name == \
                tmp and one_vm.summary.config.template == True:
            configSpec = vim.vm.ConfigSpec(annotation=str(annotation))
            task = one_vm.Reconfigure(configSpec)
            WaitForTask(task)
            print(one_vm.summary.config)
            