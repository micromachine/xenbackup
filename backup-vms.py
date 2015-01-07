#!/usr/bin/python
###################################################################
#Another Xenbackup script					  #
#G.Kurkowiak							  #
#g.kurkowiak@gmail.com						  #
###################################################################
import commands, time, logging
bdir = '/mnt/1/'
logtime = time.strftime("%y%m%d-%h%m", time.gmtime())
logger = logging.getLogger('VMneoBackup')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('/var/log/' + logtime + "-vmbackup" )
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
logger.info('Starting ...')
##For optimised vm's
def get_backup_vms():
    result = []
    result += [('2dcf9e13-b699-ea4b-b0fd-ea8dfe03593e','OK1')]
    result += [('011f8f21-790f-3145-9926-f8ed3a9fbe13','OK2')]
    return result
##For not optimised vm's (without xentools)
def get_backup_vm_special():
    result_special = []
    result_special += [('2dcf9e13-b699-ea4b-b0fd-ea8dfe03593e','SP1')]
    result_special += [('011f8f21-790f-3145-9926-f8ed3a9fbe13','SP2')]
    return result_special
def backup_vm(uuid, filename, timestamp):
    try:
	logger.info('making little snapshot of vm - be patient :' + uuid)
        cmd = "xe vm-snapshot uuid=" + uuid + " new-name-label=" + timestamp
	snapshot_uuid = commands.getoutput(cmd)
	logger.info('I think i finished snapshot ' + uuid)
    except:
	logger.error("We have a problem - it's not possible to make a snapshot of this machine" + uuid )
    try:
        logger.info('Setting parameters for : ' + uuid)
        cmd = "xe template-param-set is-a-template=false ha-always-run=false uuid=" + snapshot_uuid
        commands.getoutput(cmd)
    except:
	 logger.error("We have a problem - it's not possible to set parameters for this machine : " + uuid )
    filename = filename.replace(" ", "\ ")
    filename = filename.replace("(", "\(")
    filename = filename.replace(")", "\)")
    try: 
	logger.info('No I make export for this vm - be patient :' + uuid)
        cmd = "xe vm-export compress=true vm=" + snapshot_uuid + " filename=" + bdir + filename
        commands.getoutput(cmd)
	logger.info('Done export for vm : ' + uuid)
    except:
	logger.error("We have a problem - it's not possible to make export for this machine : " + uuid )
    try:
	logger.info('Last thin, now i must uninstall template for :' + uuid)
	cmd = "xe vm-uninstall uuid=" + snapshot_uuid + " force=true"
        commands.getoutput(cmd)
	logger.info('Done uninstaling template for vm : ' + uuid)
    except:
	logger.error("We have a problem - it's not possible to uninstall template for this machine : " + uuid )
def backup_vm_special(uuid, filename, timestamp):
    filename = filename.replace(" ", "\ ")
    filename = filename.replace("(", "\(")
    filename = filename.replace(")", "\)")
    try:
	logger.info('Shutdowning vm - be patient : ' + uuid)
        cmd = "xe vm-shutdown force=true uuid=" + uuid
	print commands.getoutput(cmd) 
	logger.info('Shutdowning vm finished : ' + uuid)
    except:
	logger.error("We have a problem - it's not possible to shuthdown this machine : " + uuid )
    try:
	logger.info('Exporting machine, be patient : ' + uuid)
        cmd = "xe vm-export compress=true filename=" + bdir + filename + " uuid=" + uuid
    	print commands.getoutput(cmd)
	logger.info('Done exporting machine : ' + uuid)
    except:
	logger.error("We have a problem - it's not possible to export this machine : " + uuid )
    try:
	logger.info('Starting machine, be patient : ' + uuid)
        cmd = "xe vm-start uuid=" + uuid
	commands.getoutput(cmd)
	logger.info('Done : Starting machine : ' + uuid)
    except:
	logger.error("We have a problem - it's not possible to start this machine : " + uuid )

if get_backup_vms():
    logger.info('Main : backup normal machine')
    for (uuid, name) in get_backup_vms():
	logger.info('Main loop for normal machine')
	timestamp = time.strftime("%y%m%d-%h%m", time.gmtime())
	print timestamp, uuid, name
	filename = name + "-" + timestamp + ".xva"
	backup_vm(uuid, filename, timestamp)
if get_backup_vms_special():
    logger.info('Main : backup special machine')
    for (uuid, name) in get_backup_vms_special():
	logger.info('Main loop for backup special machine')
	timestamp = time.strftime("%y%m%d-%h%m", time.gmtime())
	print timestamp, uuid, name
	filename = name + "-" + timestamp + ".xva"
	backup_vm_special(uuid, filename, timestamp)
