from pyVim.connect import *
import ssl

#execute script on vm with windows
def execute_script(host, user, pwd, vm_name, script_path, username_to_auth, password_to_auth):
    s= ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode = ssl.CERT_NONE
    c = SmartConnectNoSSL(host=host, user=user, pwd=pwd)
    content = c.content
    container_vms = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    
    for vm in container_vms.view:
    	if vm.name == vm_name:
    		vm_need = vm
    		tools_status = vm.guest.toolsStatus
    if (tools_status == 'toolsNotInstalled' or
                    tools_status == 'toolsNotRunning'):
        return 'true'
    creds = vim.vm.guest.NamePasswordAuthentication(
                username=username_to_auth, password=password_to_auth)
    try:
        pm = content.guestOperationsManager.processManager
        ps = vim.vm.guest.ProcessManager.ProgramSpec(programPath="C:\\Windows\\System32\\WindowsPowerShell\\V1.0\\powershell.exe",arguments=script_path)
        res = pm.StartProgramInGuest(vm_need, creds, ps)
        if res > 0:
            return 'false'
    except IOError:
    	print ("ERROR")