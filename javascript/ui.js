// various functions for interaction with ui.py not large enough to warrant putting them in separate files
var BakPrompt = "";

function gen_prompt(UpActionPrompt, UpColorPromt, UpMaterialPromt, UpProductPromt, BtActionPrompt, BtColorPromt, BtMaterialPromt, BtProductPromt, ModelTypePromt, ShoePromt, BackGroundPromt, PromptText) {
	
	var UpPromtText = "";
	if(UpActionPrompt != "None" && UpActionPrompt != "" && UpProductPromt != "None" && UpProductPromt != ""){
		UpPromtText = UpActionPrompt + " wearing "; 
	
		if(UpColorPromt != "None" && UpColorPromt != ""){
			UpPromtText = UpPromtText + UpColorPromt + " colored "; 
		}	
		if(UpMaterialPromt != "None" && UpMaterialPromt != ""){
			UpPromtText = UpPromtText + UpMaterialPromt;
		}

		UpPromtText = UpPromtText + UpProductPromt;
	}
	
	var BtPromtText = "";
	
	if(BtActionPrompt != "None" && BtActionPrompt != "" && BtProductPromt != "None" && BtProductPromt != ""){
		BtPromtText = BtPromtText + BtActionPrompt + " wearing "; 

		if(BtColorPromt != "None" && BtColorPromt != ""){
			BtPromtText = BtPromtText + BtColorPromt + " colored "; 
		}	
		if(BtMaterialPromt != "None" && BtMaterialPromt != ""){
			BtPromtText = BtPromtText + BtMaterialPromt;
		}

		BtPromtText = BtPromtText + BtProductPromt;
	}
	
	var value = "";
	if(UpPromtText != "" && BtPromtText != ""){
		value = "A person " + UpPromtText + " " + ModelTypePromt;
		value = value + ", lower body " + BtPromtText;
	}
	
	if(UpPromtText != "" && BtPromtText == ""){
		value = "A person " + UpPromtText + " " + ModelTypePromt;
	}
	
	if(UpPromtText == "" && BtPromtText != ""){
		value = "A person " + BtPromtText + " " + ModelTypePromt;
	}
	
	if(UpPromtText == "" && BtPromtText == ""){
		value = "A person " + ModelTypePromt;
	}
	
	if(ShoePromt != "None" && ShoePromt != ""){
		value = value + ", wearing " + ShoePromt;
	}
	
	if(BackGroundPromt != "None" && BackGroundPromt != ""){
		value = value + ", background in " + BackGroundPromt;
	}
	
	return value;
}

function change_model(ModelTypePromt) {
    var AsiaCheckboxA = true;
    var AsiaSliderA = 0.3;
    var AsiaCheckboxB = true;
    var AsiaSliderB = 0.3;
    var AsiaCheckboxC = true;
    var AsiaSliderC = 0.3;
    var AsianmaleCheckboxA = false;
    var AsianmaleSliderA = 0.6;
    var AsianmaleCheckboxB = false;
    var AsianmaleSliderB = 0.1;
    var EuropeCheckboxA = false;
    var EuropeSliderA = 0.3;
    var EuropeCheckboxB = false;
    var EuropeSliderB = 0.3;
    var AfricaCheckboxA = false;
    var AfricaSliderA = 0.3;
    var AfricaCheckboxB = false;
    var AfricaSliderB = 0.3;

    if (ModelTypePromt == "Woman" || ModelTypePromt == "Girl" || ModelTypePromt == "Little Girl") {

    }

    if (ModelTypePromt == "Man") {
        AsiaCheckboxA = false;
        AsiaCheckboxB = false;
        AsiaCheckboxC = false;
        AsianmaleCheckboxA = true;
        AsianmaleSliderA = 0.6;
        AsianmaleCheckboxB = true;
        AsianmaleSliderB = 0.1;
        EuropeCheckboxA = false;
        EuropeCheckboxB = false;
        AfricaCheckboxA = false;
        AfricaCheckboxB = false;
        // LatinCheckboxA = false;
    }

    if (ModelTypePromt == "Little Boy") {
        AsiaCheckboxA = false;
        AsiaCheckboxB = false;
        AsiaCheckboxC = false;
        AsianmaleCheckboxA = true;
        AsianmaleSliderA = 0.3;
        AsianmaleCheckboxB = false;
        EuropeCheckboxA = false;
        EuropeCheckboxB = false;
        AfricaCheckboxA = false;
        AfricaCheckboxB = false;
        // LatinCheckboxA = false;
    }

    if (ModelTypePromt == "Black Girl" || ModelTypePromt.includes("Black")) {
        AsiaCheckboxA = false;
        AsiaCheckboxB = false;
        AsiaCheckboxC = false;
        AsianmaleCheckboxA = false;
        EuropeCheckboxA = false;
        EuropeCheckboxB = false;
        AfricaCheckboxA = true;
        AfricaSliderA = 0.3;
        AfricaCheckboxB = true;
        AfricaSliderB = 0.3;
    }

    if (ModelTypePromt == "European Girl" || ModelTypePromt.includes("European") || ModelTypePromt.includes("Euro") || ModelTypePromt.includes("American")) {
        AsiaCheckboxA = false;
        AsiaCheckboxB = false;
        AsiaCheckboxC = false;
        AsianmaleCheckboxA = false;
        EuropeCheckboxA = true;
        EuropeSliderA = 0.3;
        EuropeCheckboxB = true;
        EuropeSliderB = 0.3;
        AfricaCheckboxA = false;
        AfricaCheckboxB = false;
    }

    return [AsiaCheckboxA, AsiaSliderA, AsiaCheckboxB, AsiaSliderB, AsiaCheckboxC, AsiaSliderC, AsianmaleCheckboxA, AsianmaleSliderA, AsianmaleCheckboxB, AsianmaleSliderB, EuropeCheckboxA, EuropeSliderA, EuropeCheckboxB, EuropeSliderB, AfricaCheckboxA, AfricaSliderA, AfricaCheckboxB, AfricaSliderB];
}

function MoldelCheckbox_change(MoldelCheckbox, AsiaCheckboxA, AsiaCheckboxB, AsiaCheckboxC, AsianmaleCheckboxA, AsianmaleCheckboxB, EuropeCheckboxA, EuropeCheckboxB, AfricaCheckboxA, AfricaCheckboxB) {
    var n = 0;
    if (AsiaCheckboxA) n++;
    if (AsiaCheckboxB) n++;
    if (AsiaCheckboxC) n++;
    if (AsianmaleCheckboxA) n++;
    if (AsianmaleCheckboxB) n++;
    if (EuropeCheckboxA) n++;
    if (EuropeCheckboxB) n++;
    if (AfricaCheckboxA) n++;
    if (AfricaCheckboxB) n++;

    if (n > 3) {
        window.alert('You can select up to 3 models only!');
        return false;
    }

    return MoldelCheckbox;
}

function ModelType_change(ModelType) {
	
	if (ModelType == 'Head and Limbs Intact') {
		console.log(ModelType);
		return [5, 0.8, ['Controller A']];
	}
	
	if (ModelType == 'Partially Missing') {
		console.log(ModelType);
		return [5, 0.6, ['Controller A']];
	}
	
	if (ModelType == 'Fully Missing') {
		console.log(ModelType);
		return [5, 0.4, ['Controller A']];
	}
	
	if (ModelType == 'Underwear') {
		console.log(ModelType);
		return [4, 0.35, ['Controller A', 'Controller B']];
	}
}

function hasClass(element,className){
	var aSameClassEle = document.getElementsByClassName(className);
	for(var i = 0;i < aSameClassEle.length;i++){
		if(aSameClassEle[i] === element){
			return true;
		}
	}
	return false;
}

function masktabs_change(){
	var m = gradioApp().querySelector('#masktabs');
	var bs = m.querySelectorAll('button');
	var i = 0;
	for(var item of bs) {
		if(!hasClass(item,'selected')){
			console.log(item.innerText)
			break;
		}
		i++;
	}
	
	return i;
}

function extract_image_from_gallery(gallery){
	//console.log(gallery)
    if(gallery.length == 1){
		switch_to_fix()
        return [gallery[0]]
    }

    index = selected_gallery_index()

    if (index < 0 || index >= gallery.length){
        return [null]
    }

		switch_to_fix()
	
    return [gallery[index]];
}

function extract_image_from_gallery_index(gallery,index){
	
	
    return gallery[index];
}

function send_one_mask(sam_input_image,sam_output_mask_gallery){
	r = [sam_input_image,extract_image_from_gallery_index(sam_output_mask_gallery,3)]
	switch_to_upload_mask()
	return r
}

function send_two_mask(sam_input_image,sam_output_mask_gallery){
	r = [sam_input_image,extract_image_from_gallery_index(sam_output_mask_gallery,4)]
	switch_to_upload_mask()
	return r
}

function send_three_mask(sam_input_image,sam_output_mask_gallery){
	r = [sam_input_image,extract_image_from_gallery_index(sam_output_mask_gallery,5)]
	switch_to_upload_mask()
	return r
}

function switch_to_upload_mask(){
	g = gradioApp().querySelector('#maintabs');
	g.querySelectorAll('button')[0].click();
	m = g.querySelector('#masktabs');
	m.querySelectorAll('button')[1].click();
}


function switch_to_gen_mask(){
	g = gradioApp().querySelector('#maintabs');
	g.querySelectorAll('button')[1].click();
}

function switch_to_fix(){
	g = gradioApp().querySelector('#maintabs');
	//console.log(g)
	g.querySelectorAll('button')[2].click();
}

function selected_gallery_index(){
    var buttons = gradioApp().querySelectorAll('[style="display: block;"].tabitem div[id$=_gallery] .thumbnail-item.thumbnail-small')
    var button = gradioApp().querySelector('[style="display: block;"].tabitem div[id$=_gallery] .thumbnail-item.thumbnail-small.selected')

    var result = -1
    buttons.forEach(function(v, i){ if(v==button) { result = i } })

    return result
}


function set_theme(theme){
    gradioURL = window.location.href
    if (!gradioURL.includes('?__theme=')) {
      //window.location.replace(gradioURL + '?__theme=' + theme);
    }
}





function args_to_array(args){
    res = []
    for(var i=0;i<args.length;i++){
        res.push(args[i])
    }
    return res
}

function switch_to_txt2img(){

    gradioApp().querySelector('#tabs').querySelectorAll('button')[0].click();

    return args_to_array(arguments);
}



function switch_to_img2img_tab(no){
    gradioApp().querySelector('#tabs').querySelectorAll('button')[1].click();
    gradioApp().getElementById('mode_img2img').querySelectorAll('button')[no].click();
}
function switch_to_img2img(){
    switch_to_img2img_tab(0);
    return args_to_array(arguments);
}

function switch_to_sketch(){
    switch_to_img2img_tab(1);
    return args_to_array(arguments);
}

function switch_to_inpaint(){
    switch_to_img2img_tab(2);
    return args_to_array(arguments);
}

function switch_to_inpaint_sketch(){
    switch_to_img2img_tab(3);
    return args_to_array(arguments);
}

function switch_to_inpaint(){
    gradioApp().querySelector('#tabs').querySelectorAll('button')[1].click();
    gradioApp().getElementById('mode_img2img').querySelectorAll('button')[2].click();

    return args_to_array(arguments);
}

function switch_to_extras(){
    gradioApp().querySelector('#tabs').querySelectorAll('button')[2].click();

    return args_to_array(arguments);
}

function get_tab_index(tabId){
    var res = 0

    gradioApp().getElementById(tabId).querySelector('div').querySelectorAll('button').forEach(function(button, i){
        if(button.className.indexOf('bg-white') != -1)
            res = i
    })

    return res
}

function create_tab_index_args(tabId, args){
    var res = []
    for(var i=0; i<args.length; i++){
        res.push(args[i])
    }

    res[0] = get_tab_index(tabId)

    return res
}

function get_img2img_tab_index() {
    let res = args_to_array(arguments)
    res.splice(-2)
    res[0] = get_tab_index('mode_img2img')
    return res
}

function create_submit_args(args){
    res = []
    for(var i=0;i<args.length;i++){
        res.push(args[i])
    }

    // As it is currently, txt2img and img2img send back the previous output args (txt2img_gallery, generation_info, html_info) whenever you generate a new image.
    // This can lead to uploading a huge gallery of previously generated images, which leads to an unnecessary delay between submitting and beginning to generate.
    // I don't know why gradio is sending outputs along with inputs, but we can prevent sending the image gallery here, which seems to be an issue for some.
    // If gradio at some point stops sending outputs, this may break something
    if(Array.isArray(res[res.length - 3])){
        res[res.length - 3] = null
    }

    return res
}

function showSubmitButtons(tabname, show){
    gradioApp().getElementById(tabname+'_interrupt').style.display = show ? "none" : "block"
    gradioApp().getElementById(tabname+'_skip').style.display = show ? "none" : "block"
}

function submit(){
    rememberGallerySelection('txt2img_gallery')
    showSubmitButtons('txt2img', false)

    var id = randomId()
    requestProgress(id, gradioApp().getElementById('txt2img_gallery_container'), gradioApp().getElementById('txt2img_gallery'), function(){
        showSubmitButtons('txt2img', true)

    })

    var res = create_submit_args(arguments)

    res[0] = id

    return res
}

function submit_img2img(){
    rememberGallerySelection('img2img_gallery')
    showSubmitButtons('img2img', false)

    var id = randomId()
    requestProgress(id, gradioApp().getElementById('img2img_gallery_container'), gradioApp().getElementById('img2img_gallery'), function(){
        showSubmitButtons('img2img', true)
    })

    var res = create_submit_args(arguments)

    res[0] = id
    res[1] = get_tab_index('mode_img2img')

    return res
}

function modelmerger(){
    var id = randomId()
    requestProgress(id, gradioApp().getElementById('modelmerger_results_panel'), null, function(){})

    var res = create_submit_args(arguments)
    res[0] = id
    return res
}


function ask_for_style_name(_, prompt_text, negative_prompt_text) {
    name_ = prompt('Style name:')
    return [name_, prompt_text, negative_prompt_text]
}

function confirm_clear_prompt(prompt, negative_prompt) {
    if(confirm("Delete prompt?")) {
        prompt = ""
        negative_prompt = ""
    }

    return [prompt, negative_prompt]
}


promptTokecountUpdateFuncs = {}

function recalculatePromptTokens(name){
    if(promptTokecountUpdateFuncs[name]){
        promptTokecountUpdateFuncs[name]()
    }
}

function recalculate_prompts_txt2img(){
    recalculatePromptTokens('txt2img_prompt')
    recalculatePromptTokens('txt2img_neg_prompt')
    return args_to_array(arguments);
}

function recalculate_prompts_img2img(){
    recalculatePromptTokens('img2img_prompt')
    recalculatePromptTokens('img2img_neg_prompt')
    return args_to_array(arguments);
}


opts = {}
onUiUpdate(function(){
	if(Object.keys(opts).length != 0) return;

	json_elem = gradioApp().getElementById('settings_json')
	if(json_elem == null) return;

    var textarea = json_elem.querySelector('textarea')
    var jsdata = textarea.value
    opts = JSON.parse(jsdata)
    executeCallbacks(optionsChangedCallbacks);

    Object.defineProperty(textarea, 'value', {
        set: function(newValue) {
            var valueProp = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value');
            var oldValue = valueProp.get.call(textarea);
            valueProp.set.call(textarea, newValue);

            if (oldValue != newValue) {
                opts = JSON.parse(textarea.value)
            }

            executeCallbacks(optionsChangedCallbacks);
        },
        get: function() {
            var valueProp = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value');
            return valueProp.get.call(textarea);
        }
    });

    json_elem.parentElement.style.display="none"

    function registerTextarea(id, id_counter, id_button){
        var prompt = gradioApp().getElementById(id)
        var counter = gradioApp().getElementById(id_counter)
        var textarea = gradioApp().querySelector("#" + id + " > label > textarea");

        if(counter.parentElement == prompt.parentElement){
            return
        }

        prompt.parentElement.insertBefore(counter, prompt)
        counter.classList.add("token-counter")
        prompt.parentElement.style.position = "relative"

		promptTokecountUpdateFuncs[id] = function(){ update_token_counter(id_button); }
		textarea.addEventListener("input", promptTokecountUpdateFuncs[id]);
    }

    registerTextarea('txt2img_prompt', 'txt2img_token_counter', 'txt2img_token_button')
    registerTextarea('txt2img_neg_prompt', 'txt2img_negative_token_counter', 'txt2img_negative_token_button')
    registerTextarea('img2img_prompt', 'img2img_token_counter', 'img2img_token_button')
    registerTextarea('img2img_neg_prompt', 'img2img_negative_token_counter', 'img2img_negative_token_button')

    show_all_pages = gradioApp().getElementById('settings_show_all_pages')
    settings_tabs = gradioApp().querySelector('#settings div')
    if(show_all_pages && settings_tabs){
        settings_tabs.appendChild(show_all_pages)
        show_all_pages.onclick = function(){
            gradioApp().querySelectorAll('#settings > div').forEach(function(elem){
                elem.style.display = "block";
            })
        }
    }
})

onOptionsChanged(function(){
    elem = gradioApp().getElementById('sd_checkpoint_hash')
    sd_checkpoint_hash = opts.sd_checkpoint_hash || ""
    shorthash = sd_checkpoint_hash.substr(0,10)

	if(elem && elem.textContent != shorthash){
	    elem.textContent = shorthash
	    elem.title = sd_checkpoint_hash
	    elem.href = "https://google.com/search?q=" + sd_checkpoint_hash
	}
})

let txt2img_textarea, img2img_textarea = undefined;
let wait_time = 800
let token_timeouts = {};

function update_txt2img_tokens(...args) {
	update_token_counter("txt2img_token_button")
	if (args.length == 2)
		return args[0]
	return args;
}

function update_img2img_tokens(...args) {
	update_token_counter("img2img_token_button")
	if (args.length == 2)
		return args[0]
	return args;
}

function update_token_counter(button_id) {
	if (token_timeouts[button_id])
		clearTimeout(token_timeouts[button_id]);
	token_timeouts[button_id] = setTimeout(() => gradioApp().getElementById(button_id)?.click(), wait_time);
}

function restart_reload(){
    document.body.innerHTML='<h1 style="font-family:monospace;margin-top:20%;color:lightgray;text-align:center;">Reloading...</h1>';
    setTimeout(function(){location.reload()},2000)

    return []
}

// Simulate an `input` DOM event for Gradio Textbox component. Needed after you edit its contents in javascript, otherwise your edits
// will only visible on web page and not sent to python.
function updateInput(target){
	let e = new Event("input", { bubbles: true })
	Object.defineProperty(e, "target", {value: target})
	target.dispatchEvent(e);
}


var desiredCheckpointName = null;
function selectCheckpoint(name){
    desiredCheckpointName = name;
    gradioApp().getElementById('change_checkpoint').click()
}
