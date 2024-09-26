import gradio as gr
import gradio.routes
import os
from io import BytesIO
from pathlib import Path
from modules import shared, scripts
from service import *
from PIL import Image

# Read image from file information
def image_from_url_text(filedata):
    if filedata is None:
        return None

    # Extract the next level data from the list
    if type(filedata) == list and len(filedata) > 0 and type(filedata[0]) == dict and filedata[0].get("is_file", False):
        filedata = filedata[0]

    # Non-data file, read the image from the file name
    if type(filedata) == dict and filedata.get("is_file", False):
        filename = filedata["name"]
        is_in_right_dir = check_tmp_file(shared.demo, filename)
        assert is_in_right_dir, 'trying to open image file outside of allowed directories'

        return Image.open(filename)

    # Further extract the next level data
    if type(filedata) == list:
        if len(filedata) == 0:
            return None

        filedata = filedata[0]

    # Convert base64 string data to image
    filedata = base64.decodebytes(filedata.encode('utf-8'))
    image = Image.open(BytesIO(filedata))
    return image

# Automatically apply mask
def fill_img_mask(imgfiledata, maskfiledata):
    maskfiledata = image_from_url_text(maskfiledata).convert('L')
    return imgfiledata, maskfiledata

# Check if the file is in the temporary folder
def check_tmp_file(gradio, filename):
    if hasattr(gradio, 'temp_file_sets'):
        return any([filename in fileset for fileset in gradio.temp_file_sets])

    if hasattr(gradio, 'temp_dirs'):
        return any(Path(temp_dir).resolve() in Path(filename).resolve().parents for temp_dir in gradio.temp_dirs)

    return False        

# Get the selected index from the event
def get_select_index(evt: gr.SelectData):
    return evt.index

# Load custom JS and replace the existing page template
def reload_javascript():
    # Main JS
    head = f'<script type="text/javascript" src="file={os.path.abspath("script.js")}?{os.path.getmtime("script.js")}"></script>\n'
    # List JS files in the "javascript" directory
    for script in scripts.list_scripts("javascript", ".js"):
        head += f'<script type="text/javascript" src="file={script.path}?{os.path.getmtime(script.path)}"></script>\n'

    # Replace the page template
    def template_response(*args, **kwargs):
        res = shared.GradioTemplateResponseOriginal(*args, **kwargs)
        res.body = res.body.replace(b'</head>', f'{head}</head>'.encode("utf8"))
        res.init_headers()
        return res

    gradio.routes.templates.TemplateResponse = template_response        

# Store the original template response if it hasn't been done already
if not hasattr(shared, 'GradioTemplateResponseOriginal'):
    shared.GradioTemplateResponseOriginal = gradio.routes.templates.TemplateResponse

# Reload the custom JS
reload_javascript()

with gr.Blocks(css="./css/style.css", title="Fashion Model Generation Platform", theme='bethecloud/storj_theme') as demo:
    with gr.Tabs(elem_id="maintabs"):  
        # Model Generation Module
        with gr.Tab("Model Generation"):
            gr.Markdown("The width and height of the uploaded image are recommended not to exceed 1024 pixels; use a mask to cover the product area.")
            with gr.Row():
                with gr.Column():
                    with gr.Tabs(elem_id="masktabs") as masktabs:  
                        with gr.Tab("Hand-drawn Mask"):
                            inp = gr.Image(label="Product", show_label=False, elem_id="img2maskimg", source="upload", interactive=True, type="pil", tool="sketch", image_mode="RGBA", brush_radius=15)
                        with gr.Tab("Upload or Generate Mask"):
                            init_img_inpaint = gr.Image(label="Product Image", source="upload", interactive=True, type="pil", elem_id="img_inpaint_base")
                            init_mask_inpaint = gr.Image(label="Mask", source="upload", interactive=True, type="pil", elem_id="img_inpaint_mask")
                            genmask_btn = gr.Button(value="Auto-generate Mask")
                        maskindex = gr.Number(show_label=False, visible=False, elem_id="maskindex", value=0.0)
                with gr.Column():
                    with gr.Group(elem_id="img2img_gallery_container"):
                        result_gallery = gr.Gallery(label='Digital Human Model', show_label=False, elem_id="img2img_gallery").style(preview=True, container=True)

            with gr.Row():
                with gr.Column():
                    with gr.Row(): 
                        gr.Markdown("Generate prompt based on selected features.")
                    with gr.Accordion('Upper Body', open=True):
                        with gr.Row():
                            UpActionPrompt = gr.Dropdown(["Wear", "Hold", "Carry", "None"], label="Action", info="How the upper body holds the item", allow_custom_value=True, elem_id="UpActionPrompt", elem_classes="PromptDropdown")
                            UpColorPromt = gr.Dropdown(["Red", "Yellow", "Blue", "Green", "Purple", "Pink", "Black", "White", "Gray", "Brown", "Khaki", "None"], label="Color", info="Color", allow_custom_value=True, elem_id="UpColorPromt", elem_classes="PromptDropdown")
                            UpMaterialPromt = gr.Dropdown(["Lace", "Transparent", "Denim", "Silk", "Cotton", "None"], label="Material", allow_custom_value=True, elem_id="UpMaterialPromt", info="Material", elem_classes="PromptDropdown")
                            UpProductPromt = gr.Dropdown(["Long Sleeve", "Short Sleeve", "Sleeveless Vest", "T-shirt", "Underwear", "Bra", "None"], label="Product", allow_custom_value=True, elem_id="UpProductPromt", interactive=True, info="Type", elem_classes="PromptDropdown")
                            
                    with gr.Accordion('General', open=True):
                        with gr.Row():
                            ModelTypePromt = gr.Dropdown(["Woman", "Girl", "Man", "Boy", "European Girl", "Black Girl"], label="Model Type", value="Woman", allow_custom_value=True, elem_id="ModelTypePromt", info="Age and type", elem_classes="PromptDropdown")
                   
                            ShoePromt = gr.Dropdown(["High Heels", "Slippers", "Sneakers", "Flats", "Long Boots", "Short Boots", "Sandals", "Leather Shoes", "None"], label="Shoes Worn", allow_custom_value=True, elem_id="ShoePromt", info="Shoes", elem_classes="PromptDropdown")
                            BackGroundPromt = gr.Dropdown(["Beach", "Park", "Garden", "Grassland", "Bedroom", "Indoor", "Mall", "Street", "In front of Eiffel Tower", "None"], label="Background", allow_custom_value=True, elem_id="BackGroundPromt", info="Background", elem_classes="PromptDropdown")
                    with gr.Accordion('Model Settings', open=False):
                        with gr.Row():
                            AsiaCheckboxA = gr.Checkbox(label='Asian Female Model A', value=True, elem_classes="ModelCheckbox", elem_id="AsiaCheckboxA")
                            AsiaSliderA = gr.Slider(label='Weight Ratio', minimum=0.1, maximum=0.9, step=0.05, value=0.3)
                        with gr.Row():
                            AsiaCheckboxB = gr.Checkbox(label='Asian Female Model B', value=True, elem_classes="ModelCheckbox", elem_id="AsiaCheckboxB")
                            AsiaSliderB = gr.Slider(label='Weight Ratio', minimum=0.1, maximum=0.9, step=0.05, value=0.3)
                        with gr.Row():
                            AsiaCheckboxC = gr.Checkbox(label='Asian Female Model C', value=True, elem_classes="ModelCheckbox", elem_id="AsiaCheckboxC")
                            AsiaSliderC = gr.Slider(label='Weight Ratio', minimum=0.1, maximum=0.9, step=0.05, value=0.3)
                        with gr.Row():
                            AsianmaleCheckboxA = gr.Checkbox(label='Male Model A', value=False, elem_classes="ModelCheckbox", elem_id="AsianmaleCheckboxA")
                            AsianmaleSliderA = gr.Slider(label='Weight Ratio', minimum=0.1, maximum=0.9, step=0.05, value=0.3)
                        with gr.Row():
                            AsianmaleCheckboxB = gr.Checkbox(label='Male Model B', value=False, elem_classes="ModelCheckbox", elem_id="AsianmaleCheckboxB")
                            AsianmaleSliderB = gr.Slider(label='Weight Ratio', minimum=0.1, maximum=0.9, step=0.05, value=0.3)
                        with gr.Row():
                            EuropeCheckboxA = gr.Checkbox(label='European Female Model A', value=False, elem_classes="ModelCheckbox", elem_id="EuropeCheckboxA")
                            EuropeSliderA = gr.Slider(label='Weight Ratio', minimum=0.1, maximum=0.9, step=0.05, value=0.3)
                        with gr.Row():
                            EuropeCheckboxB = gr.Checkbox(label='European Female Model B', value=False, elem_classes="ModelCheckbox", elem_id="EuropeCheckboxB")
                            EuropeSliderB = gr.Slider(label='Weight Ratio', minimum=0.1, maximum=0.9, step=0.05, value=0.3)
                        with gr.Row():
                            AfricaCheckboxA = gr.Checkbox(label='Black Female Model A', value=False, elem_classes="ModelCheckbox", elem_id="AfricaCheckboxA")
                            AfricaSliderA = gr.Slider(label='Weight Ratio', minimum=0.1, maximum=0.9, step=0.05, value=0.3)
                        with gr.Row():
                            AfricaCheckboxB = gr.Checkbox(label='Black Female Model B', value=False, elem_classes="ModelCheckbox", elem_id="AfricaCheckboxB")                            
                            AfricaSliderB = gr.Slider(label='Weight Ratio', minimum=0.1, maximum=0.9, step=0.05, value=0.3)

                    # Sample Images
                    gr.Examples(
                        label="Sample Images",
                        examples=[os.path.join(os.path.dirname(__file__), "./examples/1.png"),
                        os.path.join(os.path.dirname(__file__), "./examples/2.png"),
                        os.path.join(os.path.dirname(__file__), "./examples/3.png"),
                        os.path.join(os.path.dirname(__file__), "./examples/4.png"),
                        os.path.join(os.path.dirname(__file__), "./examples/5.jpg"),
                        os.path.join(os.path.dirname(__file__), "./examples/6.jpg"),
                        os.path.join(os.path.dirname(__file__), "./examples/7.png"),],
                        inputs=inp
                    )
                    
                with gr.Column(): 

                    with gr.Accordion('Lower Body', open=True):
                        with gr.Row():
                            BtActionPrompt = gr.Dropdown(["Wear", "Hold", "Carry", "None"], label="Action", info="How the lower body holds the item", allow_custom_value=True, elem_id="BtActionPrompt", elem_classes="PromptDropdown")
                            BtColorPromt = gr.Dropdown(["Red", "Yellow", "Blue", "Green", "Purple", "Pink", "Black", "White", "Gray", "Brown", "Khaki", "None"], label="Color", info="Color", allow_custom_value=True, elem_id="BtColorPromt", elem_classes="PromptDropdown")
                            BtMaterialPromt = gr.Dropdown(["Lace", "Denim", "Silk", "Chiffon", "Cotton", "Transparent", "None"], label="Material", allow_custom_value=True, elem_id="BtMaterialPromt", info="Material", elem_classes="PromptDropdown")
                            BtProductPromt = gr.Dropdown(["Long Pants", "Shorts", "Skirt", "Dress", "Strap Dress", "None"], label="Product", allow_custom_value=True, elem_id="BtProductPromt", interactive=True, info="Type", elem_classes="PromptDropdown")
                            
                    PromptText = gr.Textbox(label="Prompt", lines=3, placeholder='Enter a prompt to generate the image,  e.g., "A girl wearing a white cotton short-sleeve shirt and blue denim pants". ', elem_id="PromptText")
                    
                    with gr.Accordion('Fine-tuning Parameter Settings', open=False):
                        mask_blur = gr.Slider(label='Mask Edge Softness (smaller is closer to the original image, larger allows for more creative freedom)', minimum=4, maximum=40, step=1, value=5, elem_id="mb")
                        weight = gr.Slider(label='Control Weight (smaller allows more freedom, larger sticks closer to the original image)', minimum=0.2, maximum=1, step=0.1, value=0.5, elem_id="wei")
                        control_mode_index = gr.Radio(label='Prompt vs Controller', choices=['Balanced', 'Prompt is more important', 'Controller is more important'], value='Controller is more important', type="index", elem_id="control_mode_index", visible=True)
                        controls = gr.CheckboxGroup(['Controller A', 'Controller B', 'Controller C', 'Controller D'], label="Controllers", info="Select controllers based on image type", type="index", value=['Controller A'])
                        inpainting_mask_invert = gr.Radio(label='Generated Image Area', choices=['Inside the Mask', 'Outside the Mask'], value='Outside the Mask', type="index", elem_id="mi", visible=False)
                        inpainting_fill = gr.Radio(label='Masked Area Content', choices=['Generate New Content', 'Keep Unchanged'], value='Keep Unchanged', type="index", elem_id="if", visible=False)
                        
                    with gr.Row():
                        num = gr.Slider(label='Number of Images to Generate', minimum=1, maximum=4, step=1, value=1, visible=True)

                    perform_btn = gr.Button(value="Generate", variant='primary')

        # Auto Mask Module
        with gr.TabItem(label="Auto Mask"):
            with gr.Row():
                with gr.Column():
                    gr.HTML(value="<p>Left-click to add green dots in the product area, right-click to add red dots in non-product areas. Left-click on dots to remove them.</p>")
                with gr.Column():
                    with gr.Row():
                        gr.Markdown(value='<center><font size=5>1</font></center>')
                        gr.Markdown(value='<center><font size=5>2</font></center>')
                        gr.Markdown(value='<center><font size=5>3</font></center>')
            with gr.Row():
                with gr.Column():
                    sam_input_image = gr.Image(show_label=False, elem_id="img2img_sam_input_image", source="upload", type="pil", image_mode="RGBA")
                    with gr.Row():
                        sam_remove_dots = gr.Button(value="Clear All Dots")
                        sam_submit = gr.Button(value="Generate Mask", elem_id="img2img_sam_run_button", variant='primary')
                        sam_dummy_component = gr.Label(visible=False)
                        sam_remove_dots.click(
                            fn=lambda _: None,
                            _js="samRemoveDots",
                            inputs=[sam_dummy_component],
                            outputs=None)
                    
                with gr.Column():
                    sam_output_mask_gallery = gr.Gallery(show_label=False, label='Select Appropriate Mask', elem_id="sam_gallery").style(grid=3)
                    with gr.Row():
                        one_btn = gr.Button(value="Use Mask 1", elem_id="img2img_sam_run_button")
                        two_btn = gr.Button(value="Use Mask 2", elem_id="img2img_sam_run_button")
                        three_btn = gr.Button(value="Use Mask 3", elem_id="img2img_sam_run_button")

            gr.Examples(
                label="Sample Images",
                examples=[os.path.join(os.path.dirname(__file__), "./examples/1.png"),
                os.path.join(os.path.dirname(__file__), "./examples/2.png"),
                os.path.join(os.path.dirname(__file__), "./examples/3.png"),
                os.path.join(os.path.dirname(__file__), "./examples/4.png"),
                os.path.join(os.path.dirname(__file__), "./examples/5.jpg"),
                os.path.join(os.path.dirname(__file__), "./examples/6.jpg"),
                os.path.join(os.path.dirname(__file__), "./examples/7.png"),],
                inputs=sam_input_image
            )    
            
            sam_submit.click(
                fn=sam_predict,
                _js='submit_sam',
                inputs=[sam_input_image, 
                        sam_dummy_component, sam_dummy_component], 
                outputs=sam_output_mask_gallery,
                queue=False)
          
        # Generate Model
        perform_btn.click(fn=perform, inputs=[inp, init_img_inpaint, init_mask_inpaint, maskindex, PromptText, num, mask_blur, inpainting_mask_invert, inpainting_fill, weight, control_mode_index, AsiaCheckboxA, AsiaSliderA, AsiaCheckboxB, AsiaSliderB, AsiaCheckboxC, AsiaSliderC, AsianmaleCheckboxA, AsianmaleSliderA, AsianmaleCheckboxB, AsianmaleSliderB, EuropeCheckboxA, EuropeSliderA, EuropeCheckboxB, EuropeSliderB, AfricaCheckboxA, AfricaSliderA, AfricaCheckboxB, AfricaSliderB, controls], outputs=result_gallery)
        
        logging.info("Button perform_btn clicked and 'perform' function invoked.")

        # Prompt Generation
        UpActionPrompt.change(fn=None, _js="gen_prompt", inputs=[UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText], outputs=[PromptText], queue=False)
        UpColorPromt.change(fn=None, _js="gen_prompt", inputs=[UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText], outputs=PromptText, queue=False)
        UpMaterialPromt.change(fn=None, _js="gen_prompt", inputs=[UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText], outputs=PromptText, queue=False)
        UpProductPromt.change(fn=None, _js="gen_prompt", inputs=[UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText], outputs=PromptText, queue=False)
        
        BtActionPrompt.change(fn=None, _js="gen_prompt", inputs=[UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText], outputs=PromptText, queue=False)
        BtColorPromt.change(fn=None, _js="gen_prompt", inputs=[UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText], outputs=PromptText, queue=False)
        BtMaterialPromt.change(fn=None, _js="gen_prompt", inputs=[UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText], outputs=PromptText, queue=False)
        BtProductPromt.change(fn=None, _js="gen_prompt", inputs=[UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText], outputs=PromptText, queue=False)
        
        ModelTypePromt.change(fn=None, _js="gen_prompt", inputs=[UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText], outputs=PromptText, queue=False)
        ShoePromt.change(fn=None, _js="gen_prompt", inputs=[UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText], outputs=PromptText, queue=False)
        BackGroundPromt.change(fn=None, _js="gen_prompt", inputs=[UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText], outputs=PromptText, queue=False)

        # Multiple Model Switching
        ModelTypePromt.change(fn=None, _js="change_model", inputs=ModelTypePromt, outputs=[AsiaCheckboxA, AsiaSliderA, AsiaCheckboxB, AsiaSliderB, AsiaCheckboxC, AsiaSliderC, AsianmaleCheckboxA, AsianmaleSliderA, AsianmaleCheckboxB, AsianmaleSliderB, EuropeCheckboxA, EuropeSliderA, EuropeCheckboxB, EuropeSliderB, AfricaCheckboxA, AfricaSliderA, AfricaCheckboxB], queue=False)

        # Manual/Auto Mask Switching
        masktabs.select(fn=None, _js="masktabs_change", inputs=None, outputs=[maskindex], queue=False)

        # Auto Mask Event Response
        genmask_btn.click(
            fn=None,
            _js="switch_to_gen_mask",
            inputs=[],
            outputs=[sam_input_image], queue=False
        )
        
        # Select Auto Mask 1
        one_btn.click(
            fn=fill_img_mask,
            _js="send_one_mask",
            inputs=[sam_input_image, sam_output_mask_gallery],
            outputs=[init_img_inpaint, init_mask_inpaint], queue=False
        )
        
        # Select Auto Mask 2
        two_btn.click(
            fn=fill_img_mask,
            _js="send_two_mask",
            inputs=[sam_input_image, sam_output_mask_gallery],
            outputs=[init_img_inpaint, init_mask_inpaint], queue=False
        )

        # Select Auto Mask 3
        three_btn.click(
            fn=fill_img_mask,
            _js="send_three_mask",
            inputs=[sam_input_image, sam_output_mask_gallery],
            outputs=[init_img_inpaint, init_mask_inpaint], queue=False
        )
        

shared.demo = demo
demo.queue(concurrency_count=3).launch(server_name="0.0.0.0", server_port=8088, inbrowser=True, favicon_path="./favicon.ico")
