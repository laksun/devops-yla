import logging
import os


def get_total_memory_in_gb():
    memory_in_bytes = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    memory_in_gb = memory_in_bytes / pow(1024, 3)
    return memory_in_gb



def replace_fluenta_placeholders( fluentd_config, file , region, 
   instance_id,  http_proxy_port, target_s3_bucket,
   dest_output_conf,is_high_memory_instance, paramstore_config
):
# Add parameters to fluentd.conf fi l e 
    logging.info (f"Replacing fluentd parameters in: (file)") 
    try:
        os. rename(file, file + "-param")
    except Exception:
        logging.error ("Unable to create paramater fi l e . " ) 
        sys.exit (3)
    
    con=open(file+"-param", "r+")
    r_file = con.read()
    # Write dest_conf fi r s t because i t may also include placeholders 
    r_file = r_file.replace ("<<ADD_DESTINATION_CONFIG>>", dest_output_conf)
    r_file = r_file.replace ("<<ADD_REGION>>", region)
    r_file = r_file, replace("<<ADD_INSTANCE_ID>>", instance_id) 
    # TODO: Remove this line once al log groups are using the new placeholder below
    r_file = r_file,replace("<<HTTP_PROXY_PORI>>", str(http_proxy_port)) 
    # Remove the proxy config if a Kinesis-Firehose VPCE exists, otherwise set it to use proxy_port
    vpce = get_vpce (vpc_endpoint='firehose', param_store=paramstore_config)
    if vpce:
        r_file = r_file.replace( "<<ADD_HTTP_PROXY>",  f"endpoint {vpce}")
    elif is_vpce_enabled(vpc_endpoint='firehose'): 
        r_file = r_file.replace( "<<ADD_HTTP_PROXY>>",  "")
    else: 
        r_file = r_file.replace("<<ADD_HTTP_PROXY>",  f"h t t p - p r o x y h t t p : / / p r o x y . j p m c h a s e . n e t : { h t t p _ p r o x y _ p o r t } *")

#Removetheproxyconfigi fa CloudwatchlogsVPCEexists,otherwiseseti ttouseproxy-port 
    vpce = get_vpce(vpc_endpoint='logs', param_store=paramstore_config) 
    if vpce:
        r_file = r_file.replace('<<ADD_HTTP_PROXY_CLOUDWATCH>>",  f" e n d p o i n t { v p c e }"')
    elif is_vpce_enabled(vpc_endpoint='logs'):
        r_file = r_file.replace("<<ADD_HTTP_PROXY_CLOUDWATCH>>",  "") 
    else:
         r_file = r_file.replace( "<<ADD_HTTP_PROXY_CLOUDWATCH>›", f"http_proxyhttp://proxy-jpmchase.net:{http_proxy_port}*")
    #Increasefluentdbuffersizeo nlargerinstancest ocopewithincreasedthroughput. 
    if is_high_memory_instance:
        logging.info(f"Settingfluentdtotal_limit_sizet o1GBandflush_thread_countt o4") 
        r_file = r_file.replace("<<ADD_BUFFER_SIZE>>",  "1024MB") 
        r_file = r_file.replace("<<ADD_FLUSH_THREAD_COUNT>>",  "4")
    else:
        Logging.info(f"Settingfluentdtotal_limit_sizet o512MBandflush_thread_countt o2") 
        r_file = r_file.replace("<<ADD_BUFFER_SIZE>>",  "512MB") 
        r_file = r_file.replace( "<<ADD_FLUSH_THREAD_COUNT»>",  "2")
    if target_s3_bucket:
        r_file= r_file.replace("<<S3_APP_BUCKET»>",target_s3_bucket)
        r_file = r_file.replace( "<<ADD_S3_PATH»>",  "applogs",  1) 
        r_file = r_file.replace("<<ADD_S3_PATH>",  "codedeploylogs",  1)
    
    ncon=open(file,"w")
    ncon.write(r_file)
    con. close()
    ncon. close()
    set_file_perms(file, fluentd_config.fluentd_user, 00640)
    try:
        os.remove(file + "-param")
    except Exception:
        logging.warning("Unable to remove parameter file.")


