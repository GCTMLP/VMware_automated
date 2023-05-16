from pyVim.connect import SmartConnectNoSSL
from pyVmomi import vim
import ssl

def execute_script(host, user, pwd, vm_name, script_path, username_to_auth,
                   password_to_auth):
    '''
    execute script on vm with windows

    :param host - host ip
    :param user - esxi host user
    :param pwd - esxi host password
    :param vm_name - vm`s name
    :param script_path - path to executable script
    :param username_to_auth - vm`s username
    :param password_to_auth- vm`s password

    :return: bool
    '''
    s= ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode = ssl.CERT_NONE
    c = SmartConnectNoSSL(host=host, user=user, pwd=pwd)
    content = c.content
    container_vms = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.VirtualMachine],
                                                            True)
    for vm in container_vms.view:
        if vm.name == vm_name:
            vm_need = vm
            tools_status = vm.guest.toolsStatus
    if (tools_status == 'toolsNotInstalled' or
                    tools_status == 'toolsNotRunning'):
        return True
    creds = vim.vm.guest.NamePasswordAuthentication(
                username=username_to_auth, password=password_to_auth)
    try:
        pm = content.guestOperationsManager.processManager
        ps = vim.vm.guest.ProcessManager.\
            ProgramSpec(programPath="C:\\Windows\\System32\\WindowsPowerShell"
                                    "\\V1.0\\powershell.exe",
                        arguments=script_path)
        res = pm.StartProgramInGuest(vm_need, creds, ps)
        if res > 0:
            return False
        else:
            return True
    except IOError:
        return False
