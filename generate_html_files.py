import json
import os
from pathlib import Path

def format_array(arr):
    """Format array as comma-separated string"""
    if isinstance(arr, list):
        return ','.join(str(x) for x in arr)
    return str(arr)

def generate_html_from_json(json_path, html_path, logo_path):
    """Generate HTML file from JSON recipe data"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    recipe_name = data['recipeName']
    recipe_id = data['recipeId']
    recipe_version = data['recipeVersion']
    description = data.get('description', '')
    
    # Get quality control data
    quality_control = data.get('qualityControl', {})
    quality = quality_control.get('quality', {})
    size = quality_control.get('size', {})
    softness = quality_control.get('softness', {})
    
    # Get settings
    settings = data.get('settings', {})
    roast_level = settings.get('roastLevel', {})
    oil_level = settings.get('oilLevel', [])
    thickness = settings.get('thickness', {})
    heating = thickness.get('heating', {})
    dispensing = thickness.get('dispensing', {})
    adaptive_dak = thickness.get('adaptiveDAK', {})
    
    # Get process steps
    mixing = thickness.get('mixing', {})
    doughing = thickness.get('doughing', {})
    stabilizing = thickness.get('stabilizing', {})
    rounding = thickness.get('rounding', {})
    tractionlosscorrection = thickness.get('tractionlosscorrection', {})
    transferring = thickness.get('transferring', {})
    pressing = thickness.get('pressing', {})
    roasting = thickness.get('roasting', {})
    kicking = thickness.get('kicking', {})
    
    # Generate quality options HTML
    quality_options_html = ''
    for i, (key, val) in enumerate(quality.items(), 1):
        quality_options_html += f'''
            <div class="nested-section">
                <h4>Quality Option {i}</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div class="form-group">
                        <label>Softness</label>
                        <input type="number" step="0.01" id="quality{i}_softness" value="{val.get('softness', 0)}">
                    </div>
                    <div class="form-group">
                        <label>Roast Step</label>
                        <input type="number" id="quality{i}_roastStep" value="{val.get('roastStep', 1)}">
                    </div>
                    <div class="form-group">
                        <label>Roast Max Step</label>
                        <input type="number" id="quality{i}_roastMaxStep" value="{val.get('roastMaxStep', 2)}">
                    </div>
                    <div class="form-group">
                        <label>Note</label>
                        <input type="text" id="quality{i}_note" value="{val.get('note', '')}">
                    </div>
                </div>
            </div>'''
    
    # Generate flour ratios HTML
    flour_ratios_html = ''
    ratio_water_flour = dispensing.get('weight', {}).get('ratioWaterFlour', {})
    for i, (name, values) in enumerate(ratio_water_flour.items()):
        flour_ratios_html += f'''
            <div class="nested-section" id="flourRatio{i}">
                <div style="display: grid; grid-template-columns: 1fr 2fr auto; gap: 15px; align-items: end;">
                    <div class="form-group">
                        <label>Flour Name</label>
                        <input type="text" id="flour{i}_name" value="{name}" placeholder="e.g., Default">
                    </div>
                    <div class="form-group">
                        <label>Ratios (comma-separated)</label>
                        <input type="text" id="flour{i}_values" value="{format_array(values)}" placeholder="0.69,0.69,0.69">
                    </div>
                    <button type="button" onclick="removeFlourRatio({i})" style="padding: 10px 15px; background: #e74c3c; color: white; border: none; border-radius: 5px; cursor: pointer; height: fit-content;">Remove</button>
                </div>
            </div>'''
    
    # Generate step HTML
    def generate_step_html(step_name, step_num, step_data):
        html = f'<div class="nested-section" id="{step_name}Step{step_num}"><h4>Step {step_num}</h4><div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 20px; align-items: start;">'
        
        if 'module' in step_data:
            html += f'<div class="form-group"><label>Module</label><input type="text" id="{step_name}_{step_num}_module" value="{step_data["module"]}"></div>'
        if 'command' in step_data:
            html += f'<div class="form-group"><label>Command</label><input type="text" id="{step_name}_{step_num}_command" value="{step_data["command"]}"></div>'
        if 'vtPosition' in step_data:
            html += f'<div class="form-group"><label>VT Position (comma-separated)</label><input type="text" id="{step_name}_{step_num}_vtPosition" value="{format_array(step_data["vtPosition"])}"></div>'
        if 'vtSpeed' in step_data:
            html += f'<div class="form-group"><label>VT Speed (comma-separated)</label><input type="text" id="{step_name}_{step_num}_vtSpeed" value="{format_array(step_data["vtSpeed"])}"></div>'
        if 'knSpeed' in step_data:
            html += f'<div class="form-group"><label>KN Speed (comma-separated)</label><input type="text" id="{step_name}_{step_num}_knSpeed" value="{format_array(step_data["knSpeed"])}"></div>'
        if 'knDuration' in step_data:
            html += f'<div class="form-group"><label>KN Duration (comma-separated)</label><input type="text" id="{step_name}_{step_num}_knDuration" value="{format_array(step_data["knDuration"])}"></div>'
        if 'position' in step_data:
            html += f'<div class="form-group"><label>Position (comma-separated)</label><input type="text" id="{step_name}_{step_num}_position" value="{format_array(step_data["position"])}"></div>'
        if 'speed' in step_data:
            html += f'<div class="form-group"><label>Speed (comma-separated)</label><input type="text" id="{step_name}_{step_num}_speed" value="{format_array(step_data["speed"])}"></div>'
        if 'duration' in step_data:
            html += f'<div class="form-group"><label>Duration (comma-separated)</label><input type="text" id="{step_name}_{step_num}_duration" value="{format_array(step_data["duration"])}"></div>'
        if 'current' in step_data:
            html += f'<div class="form-group"><label>Current (comma-separated)</label><input type="text" id="{step_name}_{step_num}_current" value="{format_array(step_data["current"])}"></div>'
        if 'tolerance' in step_data:
            html += f'<div class="form-group"><label>Tolerance (comma-separated)</label><input type="text" id="{step_name}_{step_num}_tolerance" value="{format_array(step_data["tolerance"])}"></div>'
        if 'holdTime' in step_data:
            html += f'<div class="form-group"><label>Hold Time (comma-separated)</label><input type="text" id="{step_name}_{step_num}_holdTime" value="{format_array(step_data["holdTime"])}"></div>'
        if 'upPosition' in step_data:
            html += f'<div class="form-group"><label>Up Position (comma-separated)</label><input type="text" id="{step_name}_{step_num}_upPosition" value="{format_array(step_data["upPosition"])}"></div>'
        if 'upSpeed' in step_data:
            html += f'<div class="form-group"><label>Up Speed (comma-separated)</label><input type="text" id="{step_name}_{step_num}_upSpeed" value="{format_array(step_data["upSpeed"])}"></div>'
        
        html += '</div></div>'
        return html
    
    # Generate mixing steps
    mixing_html = ''
    for key in sorted(mixing.keys()):
        step_num = key.replace('step', '')
        mixing_html += generate_step_html('mixing', step_num, mixing[key])
    
    # Generate doughing steps
    doughing_html = ''
    for key in sorted(doughing.keys()):
        step_num = key.replace('step', '')
        doughing_html += generate_step_html('doughing', step_num, doughing[key])
    
    # Generate stabilizing steps
    stabilizing_html = ''
    for key in sorted(stabilizing.keys()):
        step_num = key.replace('step', '')
        stabilizing_html += generate_step_html('stabilizing', step_num, stabilizing[key])
    
    # Generate rounding steps
    rounding_html = ''
    for key in sorted(rounding.keys()):
        step_num = key.replace('step', '')
        rounding_html += generate_step_html('rounding', step_num, rounding[key])
    
    # Generate tractionlosscorrection steps
    traction_html = ''
    for key in sorted(tractionlosscorrection.keys()):
        step_num = key.replace('step', '')
        traction_html += generate_step_html('tractionlosscorrection', step_num, tractionlosscorrection[key])
    
    # Generate transferring steps
    transferring_html = ''
    for key in sorted(transferring.keys()):
        step_num = key.replace('step', '')
        transferring_html += generate_step_html('transferring', step_num, transferring[key])
    
    # Generate pressing steps
    pressing_html = ''
    for key in sorted(pressing.keys()):
        step_num = key.replace('step', '')
        pressing_html += generate_step_html('pressing', step_num, pressing[key])
    
    # Generate roasting steps
    roasting_html = ''
    for key in sorted(roasting.keys()):
        step_num = key.replace('step', '')
        roasting_html += generate_step_html('roasting', step_num, roasting[key])
    
    # Generate kicking steps
    kicking_html = ''
    for key in sorted(kicking.keys()):
        step_num = key.replace('step', '')
        kicking_html += generate_step_html('kicking', step_num, kicking[key])
    
    # Read the template HTML (crisp_roti.html)
    template_path = Path('HTML Files/crisp_roti.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace values in template
    html_content = template.replace('Crisp Roti Recipe', f'{recipe_name} Recipe')
    html_content = html_content.replace('value="1"', f'value="{recipe_id}"', 1)
    html_content = html_content.replace('value="Classic Roti"', f'value="{recipe_name}"', 1)
    html_content = html_content.replace('value="1.8.7"', f'value="{recipe_version}"', 1)
    html_content = html_content.replace('Released: wp  2025 May 24 , 11:48am', description, 1)
    
    # Replace quality options
    quality_start = html_content.find('<div id="qualityOptions"></div>')
    if quality_start != -1:
        quality_end = html_content.find('</div>', quality_start) + 6
        html_content = html_content[:quality_start] + f'<div id="qualityOptions">{quality_options_html}</div>' + html_content[quality_end:]
    
    # Replace size values
    html_content = html_content.replace('id="sizeOption1" value="0.1"', f'id="sizeOption1" value="{size.get("option1", 0.1)}"')
    html_content = html_content.replace('id="sizeOption2" value="-0.1"', f'id="sizeOption2" value="{size.get("option2", -0.1)}"')
    html_content = html_content.replace('id="sizeUpLimit" value="0.4"', f'id="sizeUpLimit" value="{size.get("upLimit", 0.4)}"')
    html_content = html_content.replace('id="sizeDownLimit" value="-0.4"', f'id="sizeDownLimit" value="{size.get("downLimit", -0.4)}"')
    
    # Replace softness values
    html_content = html_content.replace('id="softnessOption1" value="-0.08"', f'id="softnessOption1" value="{softness.get("option1", -0.08)}"')
    html_content = html_content.replace('id="softnessOption2" value="-0.04"', f'id="softnessOption2" value="{softness.get("option2", -0.04)}"')
    html_content = html_content.replace('id="softnessOption3" value="-0.01"', f'id="softnessOption3" value="{softness.get("option3", -0.01)}"')
    html_content = html_content.replace('id="softnessOption4" value="0.07"', f'id="softnessOption4" value="{softness.get("option4", 0.07)}"')
    html_content = html_content.replace('id="softnessOption5" value="0.02"', f'id="softnessOption5" value="{softness.get("option5", 0.02)}"')
    html_content = html_content.replace('id="softnessUpLimit" value="0.08"', f'id="softnessUpLimit" value="{softness.get("upLimit", 0.08)}"')
    html_content = html_content.replace('id="softnessDownLimit" value="-0.08"', f'id="softnessDownLimit" value="{softness.get("downLimit", -0.08)}"')
    
    # Replace roast level
    html_content = html_content.replace('id="roastStep" value="9"', f'id="roastStep" value="{roast_level.get("step", 9)}"')
    html_content = html_content.replace('id="roastDuration" value="1200,1500,1700,1800,1900"', f'id="roastDuration" value="{format_array(roast_level.get("duration", []))}"')
    html_content = html_content.replace('id="topRoastTemp" value="0,0,0,0,0"', f'id="topRoastTemp" value="{format_array(roast_level.get("topRoastTemp", []))}"')
    html_content = html_content.replace('id="btmRoastTemp" value="0,0,0,0,0"', f'id="btmRoastTemp" value="{format_array(roast_level.get("btmRoastTemp", []))}"')
    
    # Replace oil level
    html_content = html_content.replace('id="oilLevel" value="0.01,0.01,0.01"', f'id="oilLevel" value="{format_array(oil_level)}"')
    
    # Replace heating temperatures
    temp = heating.get('temperature', {})
    html_content = html_content.replace('id="heatingTopTemp" value="125,125,125"', f'id="heatingTopTemp" value="{format_array(temp.get("top", []))}"')
    html_content = html_content.replace('id="heatingBottomTemp" value="130,130,130"', f'id="heatingBottomTemp" value="{format_array(temp.get("bottom", []))}"')
    html_content = html_content.replace('id="heatingTopRoastTemp" value="245,245,245"', f'id="heatingTopRoastTemp" value="{format_array(temp.get("topRoast", []))}"')
    html_content = html_content.replace('id="heatingBottomRoastTemp" value="230,230,230"', f'id="heatingBottomRoastTemp" value="{format_array(temp.get("bottomRoast", []))}"')
    
    # Replace heating tolerances
    tol = heating.get('tolerance', {})
    html_content = html_content.replace('id="heatingTopTolerance" value="2,2,2"', f'id="heatingTopTolerance" value="{format_array(tol.get("top", []))}"')
    html_content = html_content.replace('id="heatingBottomTolerance" value="2,2,2"', f'id="heatingBottomTolerance" value="{format_array(tol.get("bottom", []))}"')
    html_content = html_content.replace('id="heatingTopRoastTolerance" value="5,5,5"', f'id="heatingTopRoastTolerance" value="{format_array(tol.get("topRoast", []))}"')
    html_content = html_content.replace('id="heatingBottomRoastTolerance" value="5,5,5"', f'id="heatingBottomRoastTolerance" value="{format_array(tol.get("bottomRoast", []))}"')
    
    # Replace warm tolerances
    warm_tol = heating.get('warmTolerance', {})
    html_content = html_content.replace('id="warmTopTolerance" value="5,5,5"', f'id="warmTopTolerance" value="{format_array(warm_tol.get("top", []))}"')
    html_content = html_content.replace('id="warmBottomTolerance" value="5,5,5"', f'id="warmBottomTolerance" value="{format_array(warm_tol.get("bottom", []))}"')
    html_content = html_content.replace('id="warmTopRoastTolerance" value="15,15,15"', f'id="warmTopRoastTolerance" value="{format_array(warm_tol.get("topRoast", []))}"')
    html_content = html_content.replace('id="warmBottomRoastTolerance" value="15,15,15"', f'id="warmBottomRoastTolerance" value="{format_array(warm_tol.get("bottomRoast", []))}"')
    
    # Replace dispensing weights
    weight = dispensing.get('weight', {})
    html_content = html_content.replace('id="dispensingDB" value="35,35,35"', f'id="dispensingDB" value="{format_array(weight.get("db", []))}"')
    html_content = html_content.replace('id="dispensingOil" value="2.6,2.6,3.5"', f'id="dispensingOil" value="{format_array(weight.get("oil", []))}"')
    
    # Replace dispensing tolerances
    disp_tol = dispensing.get('tolerance', {})
    html_content = html_content.replace('id="dispensingToleranceFlour" value="0.5,0.5,0.5"', f'id="dispensingToleranceFlour" value="{format_array(disp_tol.get("flour", []))}"')
    html_content = html_content.replace('id="dispensingToleranceWater" value="0.4,0.4,0.4"', f'id="dispensingToleranceWater" value="{format_array(disp_tol.get("water", []))}"')
    html_content = html_content.replace('id="dispensingToleranceOil" value="0.2,0.2,0.2"', f'id="dispensingToleranceOil" value="{format_array(disp_tol.get("oil", []))}"')
    html_content = html_content.replace('id="dispensingToleranceRatioWaterFlour" value="0.02,0.02,0.02"', f'id="dispensingToleranceRatioWaterFlour" value="{format_array(disp_tol.get("ratioWaterFlour", []))}"')
    
    # Replace flour ratios
    flour_start = html_content.find('<div id="flourRatios"></div>')
    if flour_start != -1:
        flour_end = html_content.find('</div>', flour_start) + 6
        html_content = html_content[:flour_start] + f'<div id="flourRatios">{flour_ratios_html}</div>' + html_content[flour_end:]
    
    # Replace adaptive DAK
    html_content = html_content.replace('id="adaptiveDAKHardness" value="230,240,370"', f'id="adaptiveDAKHardness" value="{format_array(adaptive_dak.get("hardness", []))}"')
    html_content = html_content.replace('id="adaptiveDAKTolerance" value="10,10,10"', f'id="adaptiveDAKTolerance" value="{format_array(adaptive_dak.get("tolerance", []))}"')
    html_content = html_content.replace('id="adaptiveDAKSlurryRange" value="150,150,160"', f'id="adaptiveDAKSlurryRange" value="{format_array(adaptive_dak.get("slurryRange", []))}"')
    
    # Replace step sections
    html_content = html_content.replace('<div id="mixingSteps"></div>', f'<div id="mixingSteps">{mixing_html}</div>')
    html_content = html_content.replace('<div id="doughingSteps"></div>', f'<div id="doughingSteps">{doughing_html}</div>')
    html_content = html_content.replace('<div id="stabilizingSteps"></div>', f'<div id="stabilizingSteps">{stabilizing_html}</div>')
    html_content = html_content.replace('<div id="roundingSteps"></div>', f'<div id="roundingSteps">{rounding_html}</div>')
    html_content = html_content.replace('<div id="tractionlosscorrectionSteps"></div>', f'<div id="tractionlosscorrectionSteps">{traction_html}</div>')
    html_content = html_content.replace('<div id="transferringSteps"></div>', f'<div id="transferringSteps">{transferring_html}</div>')
    html_content = html_content.replace('<div id="pressingSteps"></div>', f'<div id="pressingSteps">{pressing_html}</div>')
    html_content = html_content.replace('<div id="roastingSteps"></div>', f'<div id="roastingSteps">{roasting_html}</div>')
    html_content = html_content.replace('<div id="kickingSteps"></div>', f'<div id="kickingSteps">{kicking_html}</div>')
    
    # Update quality option count and flour ratio count in JavaScript
    quality_count = len(quality)
    flour_count = len(ratio_water_flour)
    html_content = html_content.replace('let qualityOptionCount = 1;', f'let qualityOptionCount = {quality_count + 1};')
    html_content = html_content.replace('let flourRatioCount = 0;', f'let flourRatioCount = {flour_count};')
    
    # Remove the initialization code that adds default options since we're pre-populating
    # We'll keep the initialization but make it conditional
    init_start = html_content.find("// Initialize form with default values")
    if init_start != -1:
        init_end = html_content.find("};", init_start) + 2
        init_code = html_content[init_start:init_end]
        # Comment out the initialization since we're pre-populating
        html_content = html_content[:init_start] + "// Form already initialized with recipe data\n" + html_content[init_end:]
    
    # Write the HTML file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated: {html_path}")

def main():
    """Generate HTML files for all recipes"""
    recipes_dir = Path('Recipes')
    html_dir = Path('HTML Files')
    logo_path = Path('logo.jpg')
    
    # Mapping of JSON files to HTML filenames
    recipe_mapping = {
        'Jowar_Bhakri.json': 'jowar_bhakri.html',
        'Masala_Poori.json': 'masala_poori.html',
        'Missi_Bhakri.json': 'missi_bhakri.html',
        'Multigrain_Poori.json': 'multigrain_poori.html',
        'Plain_Poori.json': 'plain_poori.html',
        'TGR_Poori.json': 'tgr_poori.html',
        'Tortilla_Wraps.json': 'tortilla_wraps.html'
    }
    
    for json_file, html_file in recipe_mapping.items():
        json_path = recipes_dir / json_file
        html_path = html_dir / html_file
        
        if json_path.exists():
            if not html_path.exists():
                generate_html_from_json(json_path, html_path, logo_path)
            else:
                print(f"Skipping {html_file} (already exists)")
        else:
            print(f"Warning: {json_file} not found")

if __name__ == '__main__':
    main()
