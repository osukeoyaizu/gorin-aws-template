## task1
Select a modelで「model-txt2img-stabilityai-stable-diffusion-v2-1-base」を選択する

## task2
```
deploy_parameters = {"endpoint_name":endpoint_name,"initial_instance_count":1,"instance_type":"ml.g4dn.2xlarge"}
```

## task3
```
task3_prompt = "A happy old woman with glasses sitting under a tree, photographic style, headshot, high resolution, medium length hair",

#Please change submit value to True once happy with your result for submission!
payload = {"prompt": task3_prompt, "width": 512, "height": 512, "seed": 1}
compressed_output_query_and_display(payload, "generated image with detailed prompt", submit=True, task_name='task3.png')
```

## task4
```
prompt = "a portrait of a man" #Don't modify!
negative_prompt = "beard"
payload = {"prompt": prompt, "negative_prompt": negative_prompt, "seed": 0} #Don't modify

# Once happy with your response, change the submit to True in the following line
compressed_output_query_and_display(
    payload, f"prompt: `{prompt}`, negative prompt: `{negative_prompt}`"
, submit=True, task_name='task4.png')
```

## task5
```
# Delete the SageMaker endpoint
sm_client.delete_endpoint(EndpointName = endpoint_name) 
```
