import boto3
import click
session = boto3.Session(profile_name='nouh')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []
    if project:
       #print("Project:"+project)
       filters = [{'Name':'tag:Project','Values':[project]}]
       instances = ec2.instances.filter(Filters=filters)
    else:
       instances = ec2.instances.all()
    return instances
    
    
@click.group()
def cli():

    """snapshot management"""
    
    
@cli.group('snapshots')
def snapshots():

    """snapshot management"""

@snapshots.command('list')
@click.option('--project',default=None, help="list snapshots of all instances")
def list_snapshots(project):
    "List of EC2 snapshots"
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))

    return
  
@cli.group('volumes')

def volumes():
    """Commands for instance volumes"""

@volumes.command('list')
@click.option('--project',default=None, help="list volumes of all instances")
def list_volumes(project):
    "List of EC2 volumes"
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
           print(','.join((
                v.id,
                i.id,
                v.state,
                str(v.size)+ "GiB",
                v.encrypted and "Encrypted" or "Not Encrppted"
                )))

    return

    






@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('shapshot', help="Create snapshot of all volumes")
@click.option("--project",default=None, help="only instances with project tags")
def create_snapshots(project):
    "Create snaphsots of ec2 instances"
    instances = filter_instances(project)
    for i in instances:
        i.stop()
        for v in i.volumes.all():
            print("Creating snapshot fo {0}".format(v.id))
            v.create_snapshot(Description="created by snapshotalyzer 30000")
    return
    
@instances.command('list')
@click.option('--project',default=None, help="Only instacnes with project Tag")

def list_instances(project):
    "List of EC2 instances"
    instances = filter_instances(project)
        
    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print(','.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))
    return
@instances.command('stop')
@click.option('--project',default=None, help="Only instacnes with project Tag")
def stop_instances(project):
    "Stop EC2 instances"
    instances = filter_instances(project)
    for i in instances:
        print ("Stopping {0}...".format(i.id))
        i.stop()
    return


@instances.command('start')
@click.option('--project',default=None, help="Only instacnes with project Tag")
def start_instances(project):
    "Start EC2 instances"
    instances = filter_instances(project)
    for i in instances:
        print ("Starting {0}...".format(i.id))
        i.start()
    return
        
@instances.command('do')
@click.option('--project',default=None, help="Only instances with project tags")
def do_instances(project):
    "Do statement just a test"
    print("This is just a test of `do` statement")


if __name__ == '__main__':
   cli()
