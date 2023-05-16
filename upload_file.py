from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import ssl
import requests


def upload_file(host, user, pwd, name, file, path_to_upload,username_to_auth,
				password_to_auth):
	"""
	upload file on vm by vm name

	:param host - host ip
    :param user - esxi host user
    :param pwd - esxi host password
	:param name: vm`s name
	:param file: file path on host
	:param path_to_upload:
	:param username_to_auth - vm`s username
    :param password_to_auth- vm`s password

	:return: bool
	"""
	s= ssl.SSLContext(ssl.PROTOCOL_TLSv1)
	s.verify_mode = ssl.CERT_NONE
	c = SmartConnectNoSSL(host=host, user=user, pwd=pwd)
	content = c.content
	container_vms = content.viewManager.\
		CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
	for vm in container_vms.view:
		if vm.name == name:
			vm_need = vm
			tools_status = vm.guest.toolsStatus
	if (tools_status == 'toolsNotInstalled' or
	                tools_status == 'toolsNotRunning'):
		raise SystemExit(
	                "VMwareTools is either not running or not installed. "
	                "Rerun the script after verifying that VMWareTools "
	                "is running")

	vm_path = path_to_upload
	creds = vim.vm.guest.NamePasswordAuthentication(
	            username=username_to_auth, password=password_to_auth)
	with open(file, 'rb') as myfile:
		args = myfile.read()
	try:
		file_attribute = vim.vm.guest.FileManager.FileAttributes()
		url = content.guestOperationsManager.fileManager.\
			InitiateFileTransferToGuest(vm_need, creds, vm_path,
										file_attribute, len(args), True)
		resp = requests.put(url, data=args, verify=False)    
		if not resp.status_code == 200:
			raise Exception("Error while uploading file")
		else:
			return True
	except IOError:
		raise Exception("ERROR")
	Disconnect(c)