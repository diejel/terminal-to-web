#import pywebio,re
#import asyncio
from pywebio import start_server
from pywebio import *
import pywebio
from pywebio.output import *
from pywebio.input import *
from subprocess import *
#from pywebio.session import defer_call, info as session_info, run_async
from pywebio.session import *
from pywebio.pin import *
# Read the content of the file that shows all namespaces
path_folder = '/home/dcubaz/Documents/pywebio/pyweb'
running_status = 'https://docs.emlid.com/edge/img/led-status/status_led_green_blinking.gif'
error_status = 'https://digitale22.files.wordpress.com/2014/01/exc401.gif'
pending_status = 'https://c.tenor.com/I6kN-6X7nhAAAAAj/loading-buffering.gif'
succeded_status = 'https://image.pngaaa.com/354/140354-middle.png'
unknown_status = 'https://static-00.iconduck.com/assets.00/document-unknown-icon-440x512-y6souw0o.png'
warn_status = 'https://icons.iconarchive.com/icons/3dlb/3d-vol2/256/warning-icon.png'
#pip_cmd =  "cat file1.txt"
pip_cmd = 'cat get_all_all_ns.txt'
logs_cmd = "head -n {} /var/log/auth.log".format(10)
ns_name = [ ]
pd_name = [ ]
msg_fail_pod = [ ]

from functools import partial

def row_action(choice, id):
    put_text("You click %s button with id: %s" % (choice, id))

#function get_shell_response
def get_shell_response( input_cmd, path_cwd ):
    out_cmd = check_output(input_cmd,shell=True,cwd=path_cwd)
    format_out_cmd = out_cmd.decode('utf-8')
    return format_out_cmd

#fucntion for retrieve logs
def print_log(out_msg,descr):
    code = textarea(descr, code={ 'mode': "python",  # code language
    'theme': 'cobalt', 
     }, value=out_msg )
    put_code(code, language='python')
    #return code  
ola = get_shell_response(logs_cmd,path_folder)
# Function for toast shows the log messages
#def msg_4logs(cmd,path):
    #put_text("apretaste")
    #val = print_log(cmd,path)
    #put_code(val , language='python')
#toast('New messages', position='right', color='#2188ff', duration=0, onclick=print_log)

#-----Start comment----
#Firsr group:
def  main():
        #print_log(get_shell_response(logs_cmd,path_folder),'teste')
      
        mat_str = get_shell_response(pip_cmd,path_folder)
        out_cmd = mat_str.split("\n\r\n")
        mat1 = out_cmd[0]
        print(len(out_cmd))

        for j in range(0,len(out_cmd)):
            if "pod/" in out_cmd[j]:
                print("existe pods")
                put_markdown('# Pods Section')
                mat = out_cmd[j]
                mat_hor_lines = mat.split("\n")
                mat_list = [ ]
                for p in mat_hor_lines:
                    arr = p.split()
                    if arr[3] == "Running":
                        arr.append(put_image(src=running_status,width='40px'))
                        #out_msg=get_shell_response(logs_cmd,path_folder)
                        #arr.append(put_buttons( ['view'], onclick=print_log  ) )
                        #put_code(out_msg,language='python')
                    elif arr[3] == "Succeeded":
                        arr.append(put_image(src=succeded_status,width='45px'))
                        #arr.append(put_buttons(['edit', 'delete'], onclick=partial(row_action, id=1)))

                    elif arr[3] == "Pending":
                        arr.append(put_image(src=pending_status,width='30px'))
                        #arr.append(put_buttons(['edit', 'delete'], onclick=partial(row_action, id=1)))

                    elif arr[3] == "Failed":
                        #log_captured = get_shell_response(logs_cmd,path_folder)
                        
                        ns_name_val = arr[0]; pd_name_val = arr[1].split("/")[1]
                        #msg_fail_pod_val = "Retrieving logs for pod:{}".format(pd_name_val)
                        ns_name_val = ns_name.append(ns_name_val)
                        pd_name_val = pd_name.append(pd_name_val)
                        #msg_fail_pod_val = msg_fail_pod.append(msg_fail_pod_val)
                        #print(pd_name); print(ns_name)
                        tshoot_pod = 'kubectl describe -n {} pod {}'.format(ns_name,pd_name)
                        #print_log(tshoot_pod)
                        arr.append(put_image(src=error_status,width='65px'))
                        #arr.append(put_buttons(['edit', 'delete'], onclick=partial(row_action, id=1)))

                    elif arr[3] == "Unknown":
                        arr.append(put_image(src=unknown_status,width='25px'))
                        #arr.append(put_buttons(['edit', 'delete'], onclick=partial(row_action, id=1)))

                    else:
                        arr.append("MONITORING")
                        #arr.append("LOGS")
                    mat_list.append(arr)
                put_table(mat_list)
            elif "service/" in out_cmd[j]:
                print("existe services")
                put_markdown('# Services Section')
                mat = out_cmd[j]
                mat_hor_lines = mat.split("\n")
                mat_list = [ ]
                for p in mat_hor_lines:
                    arr = p.split()
                    mat_list.append(arr)
                    #mat_list.append(style(put_text(arr),'color: black;font-size: 10px;text-align: center;padding: 10px 20px;'))
                    
                put_table(mat_list)
            elif "daemonset.apps/" in out_cmd[j]:
                print("existe daemonset.apps")
                put_markdown('# DaemonSet Section')
                mat = out_cmd[j]
                mat_hor_lines = mat.split("\n")
                mat_list = [ ]
                for p in mat_hor_lines:
                    arr = p.split()
                    try:
                        if int(arr[3]) < int(arr[2]):
                            arr.insert( 2, put_image(src=warn_status,width='50px'))
                        elif int(arr[3]) == int(arr[2]):
                            arr.insert( 2, put_image(src=succeded_status,width='50px'))
                    except:    
                            arr.insert(2,"MONITORING")
                    mat_list.append(arr)
                put_table(mat_list)
            elif "deployment.apps/" in out_cmd[j]:
                print("existe deployment.apps")
                put_markdown('# Deployment Section')
                mat = out_cmd[j]
                mat_hor_lines = mat.split("\n")
                mat_list = [ ]
                for p in mat_hor_lines:
                    arr = p.split()
                    mat_list.append(arr)
                put_table(mat_list)
            elif "replicaset.apps/" in out_cmd[j]:
                print("existe replicaset.apps")
                put_markdown('# Replicaset Section')
                mat = out_cmd[j]
                mat_hor_lines = mat.split("\n")
                mat_list = [ ]
                for p in mat_hor_lines:
                    arr = p.split()
                    try:
                        if int(arr[3]) < int(arr[2]):
                            arr.insert( 2, put_image(src=warn_status,width='50px'))
                        elif int(arr[3]) == int(arr[2]):
                            arr.insert( 2, put_image(src=succeded_status,width='50px'))
                    except:    
                            arr.insert(2,"MONITORING")
                    mat_list.append(arr)
                put_table(mat_list)
                #print_log(logs_cmd,path_folder)
                #toast('Replicaset Fail', position='right', color='#2188ff', duration=5, onclick=toast_msg_4logs(logs_cmd,path_folder))
            else:
                print("no existe pods")
                put_text("New Section")
                put_markdown('# New Section')
                mat = out_cmd[j]
                mat_hor_lines = mat.split("\n")
                mat_list = [ ]
                for p in mat_hor_lines:
                    arr = p.split()
                    mat_list.append(arr)
                put_table(mat_list)
        #print_log(tshoot_pod,msg_fail_pod)
        print(tshoot_pod)
        for k in range(0,len(pd_name)):
            print("namespace: {}, pod: {}".format(ns_name[k],pd_name[k]))
            msg_fail_pod = "[Fail Alert!] Retrieving logs for pod:{}".format(pd_name[k])
            tshoot_pod = 'kubectl describe -n {} pod {}'.format(ns_name[k],pd_name[k])
            print_log(tshoot_pod,msg_fail_pod)
        #print(pd_name)
        #print_log(tshoot_pod,msg_fail_pod)
        #print(ns_name)

        #print(msg_fail_pod)
        #pywebio.session.hold()
        #print_log("ola","teste")
if __name__ == '__main__':
     start_server(main, debug=True, port=8080, cdn=False)
     
# put_tabs([
#     {'title': 'Text', 'content': 'Hello world'},
#     {'title': 'Markdown', 'content': put_markdown('~~Strikethrough~~')},
#     {'title': 'More content', 'content': [
#         put_table([
#             ['Commodity', 'Price'],
#             ['Apple', '5.5'],
#             ['Banana', '7'],
#         ]),
#         put_link('pywebio', 'https://github.com/wang0618/PyWebIO')
#     ]},
# ])

# put_collapse('Collapse title', [
#     'text',
#     put_markdown('~~Strikethrough~~'),
#     put_table([
#         ['Commodity', 'Price'],
#         ['Apple', '5.5'],
#     ])
# ], open=True)

# put_collapse('Large text', 'Awesome PyWebIO! '*30)

# import time

# o = output("You can click the area to prevent auto scroll.")
# put_scrollable(o, height=200, keep_bottom=True)

# while 1:
#     o.append(time.time())
#     time.sleep(0.5)