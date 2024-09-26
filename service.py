import requests
import datetime
import os
import numpy as np
import gradio as gr
from util import *
import logging

# Configure logger with log level set to INFO
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # Output to the console
    ]
)

class controlnetRequest():
    def __init__(self, prompt, negative_prompt, init_image, mask, num,mask_blur,inpainting_mask_invert,inpainting_fill,size, controlnet_weight, control_mode, controlnetA, controlnetB, controlnetC, controlnetD):
        inpainting_mask_invert_FT = False 
        if inpainting_mask_invert == 0:
            inpainting_mask_invert_FT = False
        else:
            inpainting_mask_invert_FT = True
        
        print("inpainting_mask_invert_FT:" + str(inpainting_mask_invert_FT))
        print("inpainting_fill:" + str(inpainting_fill))
        print("control_mode:" + str(control_mode))
        
            
        self.url = "http://localhost:7860/sdapi/v1/img2img"
        self.body = {
            "init_images": [init_image],
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "mask": mask,
            "mask_blur": mask_blur,
            "inpainting_mask_invert": inpainting_mask_invert_FT, #Draw outside/inside the mask
            "inpainting_fill": inpainting_fill, #Mask retains original content
            "n_iter": num, #Number of generations each time
            "width": size[0],
            "height": size[1],
            "steps": 28,
            "cfg_scale": 7,
            "denoising_strength": 0.75,
            "inpaint_full_res": False, #Fullscreen redraw
            "inpaint_full_res_padding": 32,
            "seed": -1,
            "subseed": -1,
            "subseed_strength": 0,
            "batch_size": 1,
            "restore_faces": True,
            "eta": 0,
            "sampler_index": "DPM++ SDE Karras",
            "alwayson_scripts":{
                "controlnet":{
                    "args": [
                        {
                            "enabled": controlnetA,
                            "input_image": init_image,
                            "module": "softedge_hedsafe",
                            "model": "control_v11p_sd15_softedge [a8575a2a]",
                            "weight": controlnet_weight,
                            "resize_mode": "Just Resize",
                            "lowvram": False,
                            "processor_res": 768,
                            "threshold_a": 64,
                            "threshold_b": 64,
                            "guidance_start": 0.0,
                            "guidance_end": 1.0,
                            "control_mode": control_mode,
                            "pixel_perfect": True
                        },
                        {
                            "enabled": controlnetB,
                            "input_image": init_image,
                            "module": "lineart_anime",
                            "model": "control_v11p_sd15s2_lineart_anime [3825e83e]",
                            "weight": controlnet_weight,
                            "resize_mode": "Just Resize",
                            "lowvram": False,
                            "processor_res": 768,
                            "threshold_a": 64,
                            "threshold_b": 64,
                            "guidance_start": 0.0,
                            "guidance_end": 1.0,
                            "control_mode": control_mode,
                            "pixel_perfect": True
                        },
                        {
                            "enabled": controlnetC,
                            "input_image": init_image,
                            "module": "lineart_anime_denoise",
                            "model": "control_v11p_sd15s2_lineart_anime [3825e83e]",
                            "weight": controlnet_weight,
                            "resize_mode": "Just Resize",
                            "lowvram": False,
                            "processor_res": 768,
                            "threshold_a": 64,
                            "threshold_b": 64,
                            "guidance_start": 0.0,
                            "guidance_end": 1.0,
                            "control_mode": control_mode,
                            "pixel_perfect": True
                        },
                        {
                            "enabled": controlnetD,
                            "input_image": init_image,
                            "module": "pidinet_scribble",
                            "model": "control_v11p_sd15_scribble [d4ba51ff]",
                            "weight": controlnet_weight,
                            "resize_mode": "Just Resize",
                            "lowvram": False,
                            "processor_res": 768,
                            "threshold_a": 64,
                            "threshold_b": 64,
                            "guidance_start": 0.0,
                            "guidance_end": 1.0,
                            "control_mode": control_mode,
                            "pixel_perfect": True
                        }
                    ]
                    
                }
            
            }
        }

    def sendRequest(self):
        r = requests.post(self.url, json=self.body)
        return r.json()['images']       


class img2imgRequest():
    def __init__(self, prompt, negative_prompt, init_image, mask, num,fix_denoising_strength,mask_blur,inpainting_mask_invert,inpainting_fill,size):
        inpainting_mask_invert_FT = False 
        if inpainting_mask_invert == 0:
            inpainting_mask_invert_FT = False
        else:
            inpainting_mask_invert_FT = True
        self.url = "http://localhost:7860/sdapi/v1/img2img"
        self.body = {
            "init_images": [init_image],
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "mask": mask,
            "mask_blur": mask_blur,
            "inpainting_mask_invert": inpainting_mask_invert_FT, #Draw outside/inside the mask
            "inpainting_fill": inpainting_fill, #Mask retains original content
            "n_iter": num, #Number of generations each time
            "width": size[0],
            "height": size[1],
            "steps": 28,
            "cfg_scale": 7,
            "denoising_strength": fix_denoising_strength,
            "inpaint_full_res": False, #Fullscreen redraw
            "inpaint_full_res_padding": 32,
            "seed": -1,
            "subseed": -1,
            "subseed_strength": 0,
            "batch_size": 1,
            "restore_faces": True,
            "eta": 0,
            "sampler_index": "DPM++ SDE Karras",
        }

    def sendRequest(self):
        r = requests.post(self.url, json=self.body)
        
        return r.json()['images']
        

#Generate LoRA string      
def genLora(AsiaCheckboxA,AsiaSliderA,AsiaCheckboxB,AsiaSliderB,AsiaCheckboxC,AsiaSliderC,AsianmaleCheckboxA,AsianmaleSliderA,AsianmaleCheckboxB,AsianmaleSliderB,EuropeCheckboxA,EuropeSliderA,EuropeCheckboxB,EuropeSliderB,AfricaCheckboxA,AfricaSliderA,AfricaCheckboxB,AfricaSliderB):
    tempLora = ""
    if(AsiaCheckboxA):
       tempLora = tempLora + "<lora:cnGirlYcy_v10:"+ str(AsiaSliderA) + ">,"
    if(AsiaCheckboxB):
       tempLora = tempLora + "<lora:koreanDollLikeness_v15:"+ str(AsiaSliderB) + ">,"
    if(AsiaCheckboxC):
       tempLora = tempLora + "<lora:taiwanDollLikeness_v10:"+ str(AsiaSliderC) + ">,"
    if(AsianmaleCheckboxA):
       tempLora = tempLora + "<lora:bettermalebody_v1.0:"+ str(AsianmaleSliderA) + ">,"
    if(AsianmaleCheckboxB):
       tempLora = tempLora + "<lora:asianmale_v10:"+ str(AsianmaleSliderB) + ">,"
    if(EuropeCheckboxA):
       tempLora = tempLora + "<lora:europeanDollLikeness_v10:"+ str(EuropeSliderA) + ">,"
    if(EuropeCheckboxB):
       tempLora = tempLora + "<lora:Euro-AmericanDollLikeness_V20:"+ str(EuropeSliderB) + ">,"
    if(AfricaCheckboxA):
       tempLora = tempLora + "<lora:ArianaAimes_v1.0:"+ str(AfricaSliderA) + ">,"
    if(AfricaCheckboxB):
       tempLora = tempLora + "<lora:TinaKunakey:"+ str(AfricaSliderB) + ">,"

    return tempLora

def perform(init_image, init_img_inpaint, init_mask_inpaint, maskindex, prompt, num, mask_blur, inpainting_mask_invert, inpainting_fill, weight, control_mode_index, AsiaCheckboxA, AsiaSliderA, AsiaCheckboxB, AsiaSliderB, AsiaCheckboxC, AsiaSliderC, AsianmaleCheckboxA, AsianmaleSliderA, AsianmaleCheckboxB, AsianmaleSliderB, EuropeCheckboxA, EuropeSliderA, EuropeCheckboxB, EuropeSliderB, AfricaCheckboxA, AfricaSliderA, AfricaCheckboxB, AfricaSliderB, controls, progress=gr.Progress()):

    # Record initialization log
    logging.info(f"perform: Image generation started with prompt - {prompt}")
    logging.info(f"perform: Mask index - {maskindex}, Number of images - {num}")
    logging.info(f"perform: ControlNet settings: {controls}, Weights: {weight}")

    # Mask processing
    progress((0, 5), desc="Processing mask...")
    t = datetime.datetime.now().strftime('%m%d%H%M%S%f')

    os.mkdir("./out/mt/" + t)
    image = None
    mask = None
    if maskindex == 0.0:
        image = init_image['image']
        mask = init_image['mask'].convert('L')
    elif maskindex == 1.0:
        image = init_img_inpaint
        mask = init_mask_inpaint

    # Save the original image and mask
    logging.info(f"perform: Saving initial image and mask to './out/mt/{t}'")
    image.save(f"./out/mt/{t}/init_image.png")
    mask.save(f"./out/mt/{t}/mask.png")

    # Processing prompt
    progress((1, 5), desc="Processing prompt...")
    trans_prompt = "A girl, with bright smile, normal legs, normal hands, long hair"
    if not(prompt == "" or prompt is None):
        trans_prompt = prompt + ", with bright smile, normal legs, normal hands"

    logging.info(f"perform: Translated prompt - {trans_prompt}")

    # Generate LoRA model and ControlNet parameters
    lora = genLora(AsiaCheckboxA, AsiaSliderA, AsiaCheckboxB, AsiaSliderB, AsiaCheckboxC, AsiaSliderC, AsianmaleCheckboxA, AsianmaleSliderA, AsianmaleCheckboxB, AsianmaleSliderB, EuropeCheckboxA, EuropeSliderA, EuropeCheckboxB, EuropeSliderB, AfricaCheckboxA, AfricaSliderA, AfricaCheckboxB, AfricaSliderB)
    logging.info(f"perform: Generated LoRA settings - {lora}")

    control_mode = ["Balanced", "My prompt is more important", "ControlNet is more important"][control_mode_index]
    logging.info(f"perform: Control mode - {control_mode}")

    # Log control parameters and save to log file
    with open(f"./out/mt/{t}/log.txt", 'w') as file:
        file.writelines(f'prompt: {prompt}\n')
        file.writelines(f'trans_prompt: {trans_prompt}\n')
        file.writelines(f'mask_blur: {mask_blur}\n')
        file.writelines(f'inpainting_mask_invert: {inpainting_mask_invert}\n')
        file.writelines(f'inpainting_fill: {inpainting_fill}\n')
        file.writelines(f'image size: {image.size}\n')
        file.writelines(f'weight: {weight}\n')
        file.writelines(f'control_mode: {control_mode}\n')
        file.writelines(f'lora: {lora}\n')
        file.writelines(f'controlnet: {controls}\n')

    # Generating image
    try:
        progress((2, 5), desc="Generating image...")
    except Exception as e:
        logging.warning(f"Failed to update progress: {e}")

    logging.info(f"perform: Sending request to ControlNet API with prompt: {trans_prompt}")

    output_imgs_b64 = controlnetRequest(
        "photography, masterpiece, (best quality),8K, HDR, RAW photo,highres, absurdres:1.2,blurry background,"
        f"background virtualization,bokeh:1.2, lens flare,vibrant color:1.2,large depth of field,(long-focus:1.5),"
        f"{lora} {trans_prompt}",
        "badhandv4,bad-hands-5,...",
        image_to_base64(image),
        image_to_base64(mask),
        num,
        mask_blur,
        inpainting_mask_invert,
        inpainting_fill,
        image.size,
        weight,
        control_mode,
        0 in controls, 1 in controls, 2 in controls, 3 in controls
    ).sendRequest()

    logging.info("perform: Image generation completed, saving generated images.")

    # Save the generated images
    output_imgs = []
    for i, img in enumerate(output_imgs_b64):
        img_path = f"./out/mt/{t}/{i}.png"
        save_encoded_image(img, img_path)
        logging.info(f"perform: Saved generated image {i} to {img_path}")
        output_imgs.append(base64_to_image(img))

    progress((5, 5), desc="Completed!")
    logging.info("perform: Image generation process completed successfully.")
    if not output_imgs:
        logging.error("No images generated")
        return gr.update(visible=True, value="Generating image failed.")
    return output_imgs
    #return output_imgs


#Repair the image
def fix(init_image,prompt,num,denoising_strength,mask_blur,inpainting_mask_invert,inpainting_fill):

    t = datetime.datetime.now().strftime('%m%d%H%M%S%f')
    
    os.mkdir("./out/fix/" + t)
    init_image['image'].save("./out/fix/" + t + "/init_image.png")
    init_image['mask'].convert('L').save("./out/fix/" + t + "/mask.png")
    trans_prompt = "A girl in black transparent underwear, bright smile, long hair"
    if not(prompt == "" or prompt is None):
        trans_prompt = trans(prompt)
    with open ("./out/fix/"+ t + "/log.txt", 'w') as file:
        if not(prompt is None):
            file.writelines('prompt:'+ prompt + '\n')
        file.writelines('trans_prompt:'+ trans_prompt + '\n')
        file.writelines('mask_blur:'+ str(mask_blur) + '\n')
        file.writelines('inpainting_mask_invert:'+ str(inpainting_mask_invert) + '\n')
        file.writelines('inpainting_fill:'+ str(inpainting_fill) + '\n')
        file.writelines('image x:'+ str(init_image['image'].size[0]) + '\n')
        file.writelines('image y:'+ str(init_image['image'].size[1]) + '\n')
        file.writelines('denoising_strength:'+ str(denoising_strength) + '\n')
        
    output_imgs_b64 = img2imgRequest("photography, masterpiece, (best quality),8K, HDR, RAW photo,highres, absurdres:1.2,blurry background,background virtualization,bokeh:1.2, lens flare,vibrant color:1.2,large depth of field,(long-focus:1.5),"+ trans_prompt,"badhandv4,bad-hands-5,negative_hand,NSFT,nsfw,easy negative,glans,pubic hair, manboobs,paintings,sketches,(worst quality:2),(low quality:2),(normal quality:2),lowres,blurry,((monochrome)),((grayscale)),backlight,missing fingers,fewer fingers,extra fingers,extra digit,strange fingers,(fused fingers:1.61051),(too many fingers:1.61051),bad hand,bad hands,mutated hands,(poorly drawn hands:1.331),(missing arms:1.331),(extra legs:1.331),extra limbs, bad body,skin spots, acnes, skin blemishes, age spot,(ugly:1.331), (duplicate:1.331), (morbid:1.21), (mutilated:1.21), (tranny:1.331),(bad anatomy:1.21), (bad proportions:1.331), (disfigured:1.331), (more than 2 nipples:1.331),  (unclear eyes:1.331),(futa:1.1)",image_to_base64(init_image['image']), image_to_base64(init_image['mask'].convert('L')), num, denoising_strength,mask_blur,inpainting_mask_invert,inpainting_fill,init_image['image'].size).sendRequest()
    output_imgs = []
    for i,img in enumerate(output_imgs_b64):
        save_encoded_image(img, "./out/fix/"+ t + "/" + str(i) + ".png")
        output_imgs.append(base64_to_image(img))
    return output_imgs


# Auto mask
def sam_predict(input_image, positive_points, negative_points):
    sam_model_name = "sam_vit_l_0b3195.pth"

    # Check if the input image is empty
    if input_image is None:
        logging.error("sam_predict: No input image provided. Please upload an image.")
        return [], "SAM requires an input image. Please upload an image first."
    
    logging.info("sam_predict: Input image received, converting to numpy array.")

    # Convert the image to a numpy array and log the image dimensions
    image_np = np.array(input_image)
    image_np_rgb = image_np[..., :3]
    logging.info(f"sam_predict: Input image dimensions: {image_np_rgb.shape}")

    # Construct the request body
    url = "http://localhost:7860/sam/sam-predict"
    body = {
        "sam_model_name": sam_model_name,
        "input_image": image_to_base64(input_image),
        "sam_positive_points": positive_points,
        "sam_negative_points": negative_points
    }
    
    logging.info(f"sam_predict: Sending request to SAM API with model {sam_model_name} and {len(positive_points)} positive points, {len(negative_points)} negative points.")
    
    # Send the request and catch potential errors
    try:
        r = requests.post(url, json=body)
        r.raise_for_status()  # Check if the request was successful
        result = r.json()

        logging.info("sam_predict: SAM API response received successfully.")
        
    except requests.exceptions.RequestException as e:
        logging.error(f"sam_predict: Failed to send request to SAM API: {e}")
        return [], f"Request failed: {e}"

    # Process results
    output_imgs = []

    # process and log blended_images
    if "blended_images" in result:
        logging.info(f"sam_predict: Processing {len(result['blended_images'])} blended images.")
        for i, img in enumerate(result["blended_images"]):
            output_imgs.append(base64_to_image(img))
    else:
        logging.warning("sam_predict: No blended images found in SAM API response.")
    
    # process and log masks
    if "masks" in result:
        logging.info(f"sam_predict: Processing {len(result['masks'])} masks.")
        for i, img in enumerate(result["masks"]):
            output_imgs.append(base64_to_image(img))
    else:
        logging.warning("sam_predict: No masks found in SAM API response.")
    
    # procss and log masked_images
    if "masked_images" in result:
        logging.info(f"sam_predict: Processing {len(result['masked_images'])} masked images.")
        for i, img in enumerate(result["masked_images"]):
            output_imgs.append(base64_to_image(img))
    else:
        logging.warning("sam_predict: No masked images found in SAM API response.")

    logging.info("sam_predict: Image processing completed successfully.")
    
    return output_imgs
