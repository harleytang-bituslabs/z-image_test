import json
from src.application.services.assets.autonomous_complete_game.utils import (
    symbol_asset_structure, asset_structure, asset_format_string
)

# ----- decompose -----
SYMBOLS_SYSTEM_INSTRUCTION = (
    "You are an **Expert Game Asset Analyst and Prompt Engineer**. Your sole task is to meticulously and precisely isolate "
    "and describe the **core visual content of slot symbol icons** from a game rules screen."
    "Your primary directives are: "
    "1. **FOCUS:** Describe the symbol icons (the central art) ONLY. **EXCLUDE** any surrounding frames, tile backgrounds, or UI elements shown in the screenshot."
    "2. **Strict Format:** Output **ONLY** a single, valid JSON object that strictly adheres to the provided schema."
    "3. **No Commentary:** Do not include any pre-amble, explanatory text, or post-amble."
    "4. **Actionable Output:** Descriptions must be stand-alone, detailed prompts suitable for a DALL-E 3 image generation model to recreate the icon art."
)

SYMBOLS_USER_PROMPT = f"""
[TASK START]
Analyze the provided game rules screenshot. Your primary goal is to **identify and decompose** every unique symbol icon according to its designated category (High, Mid, Low, Wild, Scatter).

**Symbol Categorization & Decomposition Rules:**
1.  **Categorization:** Only categorize symbols explicitly labeled as WILD or SCATTER in the input image as such. All other symbols must be categorized as High, Mid, or Low Value.
2.  **High, Mid, and Low Value Symbols (Full Conditional Decomposition):**
    * FOCUS: Analyze all elements of the symbol—the central icon, any surrounding background or tile, and any unique text (like playing card ranks). 
    * Decomposition: Fill the 'icon' array for every symbol. For the 'integrated', 'background', and 'text' arrays, provide a detailed description only if a visually distinct asset exists for that category. If the element is absent or generic (e.g., plain white space), leave the corresponding array empty ([]).
3.  **WILD and SCATTER Symbols (FULL DECOMPOSITION):**
    * **Task 1: Integrated View:** Provide a single, comprehensive description of the **entire symbol block** (including its icon, background, and text) in the **'integrated'** array.
    * **Task 2: Decomposed View:** Provide separate, isolated descriptions for the **'icon'**, **'background'**, and **'text'** elements of that same symbol.

**Instructions for Decomposition:**
1.  **Level of Detail:** For every icon, be **hyper-specific** about the icon's color, material texture, shape, and unique visual elements.
2.  **Visual Isolation:** Treat the icon as if it were a stand-alone image. **DO NOT** describe the surrounding white space, table borders, or descriptive text shown in the rules screen.
3.  **Asset Format:** Represent each individual icon in the required format: {asset_format_string}.

[CONTEXT]
The image to analyze is the attached game rules screenshot.

[OUTPUT SCHEMA]
The final JSON object MUST strictly adhere to the provided structure:
{json.dumps(symbol_asset_structure, indent=2)}
All descriptions MUST be contained within the 'description' field of the nested dictionary."""

MAINSCENES_SYSTEM_INSTRUCTION = (
    "You are an **Expert Game Asset Analyst and Prompt Engineer**. Your primary directives are: "
    "1. **STRICT JSON:** Output **ONLY** a single, valid JSON object strictly adhering to the provided schema. "
    "2. **CRITICAL EXCLUSION:** **DO NOT** analyze or describe the central pictorial content of the primary slot symbols (High, Mid, Low, Wild, Scatter) found within the main reel grid. Treat those areas as simple containers for context analysis only."
    "3. **ISOLATION DIRECTIVE:** For 'characters', **ONLY** generate descriptions of the character itself, isolated from any frame, background, or accessory component. "
    "4. **NO COMMENTARY:** Do not include any pre-amble, explanatory text, or post-amble outside of the JSON block."
)

MAINSCENES_USER_PROMPT = f"""
[TASK START]
Analyze the provided slot game main scene screenshot meticulously. Your primary goal is to decompose every visible asset according to the four specified high-level categories (Symbols, UI, Backgrounds, Characters).

**Decomposition Instructions:**

### CATEGORY SPECIFIC RULES:
1. **Characters -> main_game -> portrait:** The description must generate the character/mascot **ONLY**.
    * **Goal:** Generate a detailed, full-body depiction of the character, isolated from any background or frame.
    * **Aspect Ratio Logic (Crucial):**
        * IF a full-body view of the character (regardless of species—humanoid, animal, or creature) requires a vertical canvas to prevent cropping or loss of detail (e.g., for standing humans, tall animals, or vertical structures): **STRICTLY USE 1024x1536 (Vertical Portrait).**
        * OTHERWISE (e.g., for seated characters, short/wide mascots): **PREFER 1024x1024 (Square) or 1536x1024 (Horizontal Landscape).**
2.  **Backgrounds -> panels -> gameplay/popup:** Generate two distinct asset types: the **frame-only** asset (inner and outer area should be transparent, the filename MUST ends with '_frameonly') and the **frame-plus-background** asset. **For the frame-plus-background asset, the filename MUST end with '_filled', the description MUST ensure the inner space of the frame or panel is completely filled and opaque (not transparent).**. **MANDATORY: AT LEAST ONE ASSET MUST BE THE MAIN SLOT MACHINE FRAME. The description for this main frame MUST ensure the inner area is completely hollow and transparent (without any visual lines, borders, or guides for the internal symbol grid).**
3.  **Backgrounds -> background -> scene:** The scene description must ensure the generated image **fills the entire output canvas from edge to edge. Strictly exclude any borders, padding, fade-out, or vignette effects. (No transparency, No gray edges, No unrendered space)**.
4.  **Backgrounds -> background -> slot_grid:** **MANDATORY: Generate a description for EVERY SEEN DIFFERENT SQUARE-SHAPE GRID UNIT background that will be used inside the slot machine frame.**
5.  **UI -> fonts -> digits:** Generate one single description that meticulously details the entire set of numeric and currency characters: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, $, . (period), , (comma). The description must specify the exact style, color, texture, and effect (e.g., golden metallic, glowing, 3D beveled serif font) that applies universally to all 14 characters, ensuring they can be generated together with perfect style consistency.
6.  **UI -> buttons -> icons:** Descriptions in this list should **ONLY** generate the icon or graphical element that sits *on top* of the button, **DO NOT include any frames or background, must be ICON ONLY**.
7.  **UI -> buttons -> button_base:** Descriptions in this list should **ONLY** generate the empty button base, including its border and **OPAQUE (NON-TRANSPARENT)** background, ready to receive an icon.
8.  **UI: For any asset that is text-based (UI->fonts->logo or UI-fonts-text) but not part of the universal digit set (UI-fonts-digit), the description MUST clearly state the exact text content represented by the asset using this template: **The text 'text-need-to-be-generated' in a [all the other description]**. The generated text MUST stand alone. DO NOT include any backgrounds, frames, plaques, or solid color fields. For logo assets, a wide-rectangle layout is preferred over a square layout.

### FORMAT & DETAIL:
* **Level of Detail:** Be **hyper-specific** about color, texture, shape, style, and placement.
* **Asset Format:** Represent each individual visible asset in the required format: {asset_format_string}.

[CONTEXT]
The image to analyze is the attached main scene game screenshot.

[OUTPUT SCHEMA]
The final JSON object MUST strictly adhere to the provided structure:
{json.dumps(asset_structure, indent=2)}
"""

POPUPS_SYSTEM_INSTRUCTION = (
    "You are an **Expert Game Asset Analyst and Prompt Engineer** specializing in popup interface decomposition. "
    "Your primary directives are: "
    "1. **STRICT JSON:** Output **ONLY** a single, valid JSON object that strictly adheres to the provided schema. "
    "2. **ISOLATION DIRECTIVE:** For 'characters', **ONLY** generate descriptions of the character itself, isolated from any frame, background, or accessory component. "
    "3. **NO COMMENTARY:** Do not include any pre-amble, explanatory text, or post-amble outside of the JSON block. "
)

POPUPS_USER_PROMPT = f"""
[TASK START]
Analyze the provided game screenshot. This image displays a **single, modal popup message**.

**Analysis Scope:**
1.  **EXCLUDE:** Completely ignore any partially visible elements from the main game or background scene (e.g., the slot grid, main logo, side decorations).
2.  **FOCUS:** Concentrate entirely on the popup's title, text, digits, frames, background panels, **and all illustrative characters and props**.

**Decomposition Instructions:**

### CATEGORY SPECIFIC RULES:
1. **Characters -> main_game -> portrait:** The description must generate the character/mascot **ONLY**. **OR** the character with their primary prop.
    * **Goal:** Generate a detailed, full-body depiction of the character, isolated from any background or frame. If the character is holding or closely interacting with a significant, identifiable prop, a second description MUST be created for the character including that prop. Each description must ensure the character and prop are isolated from any other background or frame
    * **Aspect Ratio Logic (Crucial):**
        * IF a full-body view of the character (regardless of species—humanoid, animal, or creature) requires a vertical canvas to prevent cropping or loss of detail (e.g., for standing humans, tall animals, or vertical structures): **STRICTLY USE 1024x1536 (Vertical Portrait).**
        * OTHERWISE (e.g., for seated characters, short/wide mascots): **PREFER 1024x1024 (Square) or 1536x1024 (Horizontal Landscape).**
2.  **Backgrounds -> panels -> gameplay/popup:** Generate two distinct asset types: the **frame-only** asset (inner and outer area should be transparent, the filename MUST ends with '_frameonly') and the **frame-plus-background** asset. **For the frame-plus-background asset, the filename MUST end with '_filled', the description MUST ensure the inner space of the frame or panel is completely filled and opaque (not transparent).**.
3.  **UI -> fonts -> digits:** Generate one single description that meticulously details the entire set of numeric and currency characters: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, $, . (period), , (comma). The description must specify the exact style, color, texture, and effect (e.g., golden metallic, glowing, 3D beveled serif font) that applies universally to all 14 characters, ensuring they can be generated together with perfect style consistency.
4.  **UI -> buttons -> icons:** Descriptions in this list should **ONLY** generate the icon or graphical element that sits *on top* of the button, **DO NOT include any frames or background, must be ICON ONLY**.
5.  **UI -> buttons -> button_base:** Descriptions in this list should **ONLY** generate the empty button base, including its border and background, ready to receive an icon.
6.  **UI: For any asset that is text-based (UI->fonts->logo or UI-fonts-text) but not part of the universal digit set (UI-fonts-digit), the description MUST clearly state the exact text content represented by the asset using this template: **The text 'text-need-to-be-generated' in a [all the other description]**. The generated text MUST stand alone. DO NOT include any backgrounds, frames, plaques, or solid color fields. For logo assets, a wide-rectangle layout is preferred over a square layout.

### FORMAT & DETAIL:
* **Level of Detail:** Be **hyper-specific** about color, texture, shape, style, and placement.
* **Asset Format:** Represent each individual visible asset in the required format: {asset_format_string}.

[CONTEXT]
The image to analyze is the attached popup screenshot.

[OUTPUT SCHEMA]
The final JSON object MUST strictly adhere to the provided structure:
{json.dumps(asset_structure, indent=2)}
"""

# ----- audio decomposition/generation -----
def get_audio_asset_instructions():
    system_instruction = ("""
        You are an expert Game Audio Director. Your task is to analyze the provided video clip of a game scene 
        and determine the best possible Background Music (BGM) and Sound Effects (SFX) required to enhance 
        the player experience.
        
        **BGM Analysis (TWO Separate Tracks Required):**
        - You must generate two distinct BGM assets: **BGM_Normal** and **BGM_Freespin**.
        - **BGM_Normal:** Determine the overall mood, genre, and pace of the scene.
        - **BGM_Freespin:** This track must be an exciting, faster, and more intense variation of the Normal BGM to signal a bonus round.
        - For both tracks, write two descriptive prompts (Prompt1 and Prompt2) that capture the required musical style. Prompt1 is primary. Prompt2 can be empty if not needed.
        - **Constraint:** Weight values (weight1, weight2) must be in the range (0.0, 2.0].
        - Determine an appropriate BPM (Beats Per Minute) for each track. The Freespin BPM must be higher than the Normal BPM.
        - Provide a unique filename for each track, clearly indicating 'normal' or 'freespin'.
        
        **SFX Analysis (Multiple Tracks):**
        - Identify all critical user interactions or visual events that require a sound effect (e.g., button clicks, item collection, enemy hit, successful action).
        - For each required SFX, create a detailed, multi-sentence prompt. **The first sentence of the prompt must be a brief description ending in a period (.)**, as this will be used for the brief description field.
        - **Constraint:** Duration (duration_seconds) must be in the range [0.5, 30].
        - Determine a realistic duration (in seconds) for each SFX.
        - Provide a unique filename for each SFX.
        
        Your output MUST be a single JSON object strictly following the provided schema. DO NOT include any text outside the JSON block.
    """)

    user_prompt = f"Analyze the attached video file. Based on the actions and visuals, provide the required BGM assets (Normal and Freespin) and a list of all necessary SFX asset descriptions for this scene.Ensure the output strictly adheres to the JSON schema."
    return system_instruction, user_prompt

# ----- re-design -----
def get_redesign_symbols_instructions(game_story_design_data, decompose_data):
    """
    Generates prompts for redesigning the slot symbol assets found in the rules screen.
    """
    REDESIGN_SYMBOLS_SYSTEM_INSTRUCTION = (
        "You are an **Expert Game Asset Rewriter and Prompt Engineer**. Your sole task is to rewrite the visual descriptions "
        "of slot symbol assets. The original assets were described based on a screenshot of a game's symbol rules table."
        "Your primary directives are: "
        "1. **STRICT JSON:** Output **ONLY** a single, valid JSON object that strictly adheres to the structure of the 'ASSET BLUEPRINT'. "
        "2. **PRESERVATION:** Preserve the EXACT structure, including all keys like 'filename', 'symbol_type', and nested arrays."
        "3. **REWRITE FOCUS:** For every asset object, you MUST rewrite the **'description_for_generator'** field to strictly conform to the new visual style and theme defined in the 'NEW GAME STORY DESIGN'."
        "4. **NO COMMENTARY:** Do not include any pre-amble, explanatory text, or post-amble outside of the JSON block."
    )

    REDESIGN_SYMBOLS_USER_PROMPT = f"""
    [TASK START]
    Rewrite the asset descriptions in the 'ASSET BLUEPRINT' JSON. The new descriptions must transform the original symbol concepts to match the visual and thematic style defined in the 'NEW GAME STORY DESIGN'.

    **Example Transformation Principle:**
    If the ASSET BLUEPRINT has a 'Low Value Symbol' described as "A simple red cherry icon," and the NEW GAME STORY DESIGN has a theme of "Cyberpunk Dystopia," the new 'description_for_generator' should be rewritten to something like: "A glitching, low-resolution pixel art image of a neon-magenta skull, reflecting the analog static of a dying screen."

    [NEW GAME STORY DESIGN (Style Guide)]
    {json.dumps(game_story_design_data, indent=2)}

    [ASSET BLUEPRINT (Symbol Data to be Transformed)]
    {json.dumps(decompose_data, indent=2)}

    GENERATE ONLY THE REDESIGNED JSON OBJECT NOW.
    """
    return REDESIGN_SYMBOLS_SYSTEM_INSTRUCTION, REDESIGN_SYMBOLS_USER_PROMPT

def get_redesign_mainscene_instructions(game_story_design_data, decompose_data):
    """
    Generates prompts for redesigning all UI, frames, backgrounds, and characters 
    visible in the main gameplay screen.
    """
    REDESIGN_MAINSCENES_SYSTEM_INSTRUCTION = (
        "You are an **Expert Game UI and Environment Prompt Engineer**. Your task is to rewrite all visual descriptions for "
        "the main scene's assets, backgrounds, and frames based on a new creative mandate."
        "Your primary directives are: "
        "1. **STRICT JSON:** Output **ONLY** a single, valid JSON object that strictly adheres to the structure of the 'ASSET BLUEPRINT'."
        "2. **PRESERVATION:** Preserve the EXACT JSON structure, keys, and values of the 'ASSET BLUEPRINT', including 'filename', nested arrays, and category keys."
        "3. **REWRITE FOCUS:** For every asset object, you MUST rewrite the **'description_for_generator'** field to strictly conform to the new color, material, and thematic style defined in the 'NEW GAME STORY DESIGN'."
        "4. **LAYOUT CONTEXT:** The attached image provides critical context for asset layout, size, and function. The redesigned descriptions must maintain the original asset's purpose."
        "5. **NO COMMENTARY:** Do not include any pre-amble, explanatory text, or post-amble outside of the JSON block."
    )

    REDESIGN_MAINSCENES_USER_PROMPT = f"""
    [TASK START]
    Rewrite the asset descriptions in the 'ASSET BLUEPRINT' JSON below. The new descriptions must transform the assets to match the visual and thematic style defined in the 'NEW GAME STORY DESIGN'.

    **Key Transformation Rules:**
    * **Character Redesign:** The description for the character asset must generate the character/mascot **ONLY**. If the asset represents a human or humanoid, the description **MUST** detail the **full body** (isolated from any frame or background).
    * **Text and Fonts:** Preserve the **exact text content** (e.g., 'CREDIT', 'BET', 'WIN') from the original asset, but rewrite the styling (color, typeface, texture, effects) to strictly match the new game's theme.
    * **Color/Theme:** Update all metallic/material descriptions (borders, panels, bases) to match the `color_palette` and `geology_feature` described in the new main scene design.
    * **Scene:** The background scene description must strictly adhere to the new `scene_name`, `geology_feature`, and `color_palette`.

    [NEW GAME STORY DESIGN (Style Guide)]
    {json.dumps(game_story_design_data, indent=2)}

    [ASSET BLUEPRINT (Main Scene Data to be Transformed)]
    {json.dumps(decompose_data, indent=2)}

    GENERATE ONLY THE REDESIGNED JSON OBJECT NOW.
    """
    return REDESIGN_MAINSCENES_SYSTEM_INSTRUCTION, REDESIGN_MAINSCENES_USER_PROMPT

def get_redesign_popups_instructions(game_story_design_data, decompose_data):
    """
    Generates prompts for redesigning all UI, frames, and background assets 
    visible in the popups/modal screens.
    """
    REDESIGN_POPUPS_SYSTEM_INSTRUCTION = (
        "You are an **Expert Game UI and Modal Prompt Engineer**. Your task is to rewrite all visual descriptions for "
        "the game's modal and popup elements based on a new creative mandate."
        "Your primary directives are: "
        "1. **STRICT JSON:** Output **ONLY** a single, valid JSON object that strictly adheres to the structure of the 'ASSET BLUEPRINT'."
        "2. **PRESERVATION:** Preserve the EXACT JSON structure, keys, and values of the 'ASSET BLUEPRINT', including 'filename', nested arrays, and category keys."
        "3. **REWRITE FOCUS:** For every asset object, you MUST rewrite the **'description_for_generator'** field to strictly conform to the new color, material, and thematic style defined in the 'NEW GAME STORY DESIGN'."
        "4. **LAYOUT CONTEXT:** The attached image provides critical context for the popup's composition, shape, and internal panel structure. The redesigned descriptions must maintain the original asset's purpose."
        "5. **NO COMMENTARY:** Do not include any pre-amble, explanatory text, or post-amble outside of the JSON block."
    )

    REDESIGN_POPUPS_USER_PROMPT = f"""
    [TASK START]
    Rewrite the asset descriptions in the 'ASSET BLUEPRINT' JSON below. The new descriptions must transform the modal panels, borders, buttons, and text elements to match the visual and thematic style defined in the 'NEW GAME STORY DESIGN'.

    **Key Transformation Rules:**
    * **Character Redesign:** The description for the character asset must generate the character/mascot **ONLY**. If the asset represents a human or humanoid, the description **MUST** detail the **full body** (isolated from any frame or background).
    * **Text and Fonts:** Preserve the **exact text content** (e.g., 'CREDIT', 'BET', 'WIN') from the original asset, but rewrite the styling (color, typeface, texture, effects) to strictly match the new game's theme.
    * **Color/Theme:** Update all borders and panel fills (especially those with '_filled' filenames) to align with the new game's aesthetic and color palette (e.g., transforming 'Glossy Gold' into 'Rusted Copper' if the theme is 'Post-Apocalyptic').
    * **Structure:** Maintain the distinction between '_frameonly' (transparent inner area) and '_filled' (opaque inner area) assets.

    [NEW GAME STORY DESIGN (Style Guide)]
    {json.dumps(game_story_design_data, indent=2)}

    [ASSET BLUEPRINT (Popup Scene Data to be Transformed)]
    {json.dumps(decompose_data, indent=2)}

    GENERATE ONLY THE REDESIGNED JSON OBJECT NOW.
    """
    return REDESIGN_POPUPS_SYSTEM_INSTRUCTION, REDESIGN_POPUPS_USER_PROMPT

def get_redesign_audio_asset_instructions(game_story_design_data, decompose_data):
    REDESIGN_AUDIO_SYSTEM_INSTRUCTION = (
        "You are an **Expert Game Composer and Sound Designer Prompt Engineer**. Your task is to rewrite the audio descriptions "
        "to reflect a new creative mandate. You must transform the original audio concepts to match the new game's theme, mood, and pace."
        "Your primary directives are: "
        "1. **STRICT JSON:** Output **ONLY** a single, valid JSON object that strictly adheres to the structure of the 'ASSET BLUEPRINT'."
        "2. **PRESERVATION:** Preserve the EXACT structure, keys, and values of the 'ASSET BLUEPRINT', including 'filename', 'weight', and 'duration_seconds'."
        "3. **REWRITE FOCUS (BGM):** For BGM tracks, rewrite both **'prompt1'** and **'prompt2'** to match the genre and mood of the new story design. You must also adjust the **'bpm'** field to reflect the new theme (Freespin BPM must be higher than Normal BPM)."
        "4. **REWRITE FOCUS (SFX):** For SFX tracks, rewrite the **'description'** field to maintain the sound's original function (e.g., button click) but apply the new thematic sound (e.g., transforming a 'coin clink' to a 'synth ripple'). The first sentence of the new description MUST be a brief summary ending in a period (.)."
        "5. **LAYOUT CONTEXT:** The attached video clip provides critical temporal context (timing, pacing, and visual action) for the original BGM and SFX placement. Use this context to inform the redesigned prompts."
        "6. **NO COMMENTARY:** Do not include any pre-amble, explanatory text, or post-amble outside of the JSON block."
    )

    REDESIGN_AUDIO_USER_PROMPT = f"""
    [TASK START]
    Rewrite the audio asset descriptions in the 'ASSET BLUEPRINT' JSON below. The new descriptions must transform the BGM and SFX assets to match the sound and mood of the 'NEW GAME STORY DESIGN'.

    **Key Transformation Rules:**
    * **BGM Pacing:** Analyze the video clip to determine the general pace and mood of the original game's normal and bonus rounds. Update the musical genre, instrumentation, and overall mood (prompts) to match the new story and character, ensuring the **Freespin track is faster and more intense** than the Normal track, and the **BPMs are adjusted** accordingly.
    * **SFX Texture:** Maintain the functional purpose of the sound (e.g., a spin button sound) but change its sonic texture to fit the new aesthetic (e.g., changing 'chime' to 'mechanical grind' or 'digital glitch').

    [NEW GAME STORY DESIGN (Style Guide)]
    {json.dumps(game_story_design_data, indent=2)}

    [ASSET BLUEPRINT (Audio Data to be Transformed)]
    {json.dumps(decompose_data, indent=2)}

    GENERATE ONLY THE REDESIGNED JSON OBJECT.
    """
    return REDESIGN_AUDIO_SYSTEM_INSTRUCTION, REDESIGN_AUDIO_USER_PROMPT

# ----- validation -----
DIGIT_EXTRACTOR_SYSTEM_INSTRUCTION = (
    "You are a **Precise Character Extractor**. Your sole task is to visually identify and list every unique character (digits and symbols) present in the image. "
    "1. **Strict Output:** Output **ONLY** a single, valid JSON object strictly adhering to the provided schema."
    "2. **No Commentary:** Do not include any pre-amble, explanatory text, or post-amble outside of the JSON block."
    "3. **Order:** List characters in a logical reading order (left-to-right, top-to-bottom)."
)

DIGIT_EXTRACTOR_USER_PROMPT = f"""
[TASK]
Analyze the attached image. It contains a collection of individual numeric and currency characters.

**Your goal is to:**
1.  Identify **every unique character** (letters, digits, dollar sign, comma, period) you can visually confirm.
2.  Provide a **brief visual note** on the overall style and clarity of the characters.

[OUTPUT SCHEMA INSTRUCTIONS]
The final JSON object MUST strictly adhere to the provided Pydantic schema for `DigitValidationOutput`.
"""

def get_character_extractor_prompts(description=None):
    if description is not None:
        CHAR_EXTRACTOR_SYSTEM_INSTRUCTION = (
            "You are an **Expert Asset Validator and Quality Control Auditor**. Your sole task is to determine the fidelity "
            "of a text-based image asset against its original generation prompt. You must perform two steps: "
            "1. **Extraction:** Precisely identify the complete list of target text strings (characters, words, or phrases) required by the prompt. "
            "2. **Validation:** Visually inspect the input image to confirm the presence, accuracy, and completeness of *every* extracted target string. "
            "Your output MUST be a single, valid JSON object following the provided schema, and you MUST provide a detailed reason for any failure. "
        )
        CHAR_EXTRACTOR_USER_PROMPT = f"""
        [TASK START]
        Analyze the provided image against its generation prompt.

        ### Part A: Text Extraction (Logic)
        Analyze the prompt below to extract **ALL** text required to be in the image. The required text is always enclosed in single quotes ('...'). 
        Example: From "The text 'GRAND', 'MAJOR', 'MINOR' in a bold..." you must extract ['GRAND', 'MAJOR', 'MINOR'].

        ### Part B: Visual Validation (Criteria)
        Audit the input image against the extracted text list based on the following **STRICT** rules:
        1. **🚫 NO CROPPING (MANDATORY FAILURE):** This is the single most critical rule.
            * **Failure Definition:** If ANY part of a required text string (including the text body, outline, or shadow) is **TOUCHING OR CUT OFF** by the image border, the entire validation **FAILS**.
            * **Penalty:** Do not logically complete the word. If the word 'ANYWHERE' is required, but 'A' or 'E' is cropped, you **must** conclude the word 'ANYWHERE' is **NOT** present in full.
        2. **LITERAL COMPLETENESS:** The text generated in the image **MUST be an exact, literal match** to the required string, including all punctuation, symbols, and casing (e.g., 'CONGRATULATIONS!' required, 'CONGRATULATION' generated = FAIL).
        3. **Accuracy:** Is every generated text string accurate? (e.g., No missing characters like 'B' generating as 'P'; no merged characters like 'r' and 'n' merging into 'm'.)
        4. **🚫 NO CHARACTER MERGING/CORRUPTION (MANDATORY FAILURE):** **Each character must stand as a distinct and separate unit.**
            * **Failure Definition:** If two or more intended characters (e.g., 'U' and 'L') are visually fused, joined, or overlapping to the point that they form a single, indistinguishable shape or are structurally corrupted, the word **FAILS**. The required character list is not met.
        5. **No Artifacts:** Is the text clean, legible, and free of generation errors?

        [INPUT DATA]
        - **Generation Prompt:** "{description}"
        - **Input Image:** [The attached image file]

        [OUTPUT SCHEMA]
        {{
          "passed": true/false,
          "required_text_list": ["list", "of", "all", "extracted", "text"],
          "detected_text_list": ["list of all visually confirmed text. IMPORTANT: If a character is cropped, missing, or corrupted, that character MUST be omitted in the reported word. **DO NOT logically complete the word or phrase.** (e.g., if 'PRESS ANYWHERE' is required, but 'A' and 'E' are cropped, report ['PRESS [CROP]NYWHER[CROP]'] or similar representation of the visual truth, not ['PRESS ANYWHERE']).""],
          "error_details": "Provide detailed reason for failure (e.g., 'Validation FAILED due to text cropping. The word 'ANYWHERE' is cut off.' or 'Validation FAILED due to literal mismatch. Required: ! but was not generated.'). If passed, state: 'N/A'"
        }}
        """
        return CHAR_EXTRACTOR_SYSTEM_INSTRUCTION, CHAR_EXTRACTOR_USER_PROMPT
    else:
        return DIGIT_EXTRACTOR_SYSTEM_INSTRUCTION, DIGIT_EXTRACTOR_USER_PROMPT

# ----- retry -----
def get_background_enhanced_instructions(original_description):
    system_instruction = (
        "You are an expert AI prompt engineer specializing in stable diffusion "
        "and generative art composition. Your task is to analyze a failed "
        "image generation prompt for a game background scene. The **FAILURE MODE** "
        "is that the generated image **did not fill the entire output canvas** "
        "(i.e., it had borders, fade-outs, or transparent areas). "
        "Your goal is to **rewrite the prompt** to strictly enforce a **FULL-BLEED** "
        "composition. You must identify and mitigate high-risk components (like 'dusk,' 'silhouette,' 'fog,' or 'vignette' tendencies). "
        "**The rewritten prompt must be as similar to the original as possible, only adding necessary full-bleed and clarity components.** "
        "**Output ONLY the enhanced prompt text, nothing else.**"
    )
    
    user_prompt = f"""
    Original Failed Description: "{original_description}"
    Instructions for Rewrite:
    1. Maintain the core visual elements and style of the Original Description.
    2. Analyze for high-risk words (e.g., 'dusk', 'silhouette', 'haze', 'gradient') and replace them or clarify them to prevent fade-out.
    3. Insert mandatory full-bleed instructions using strong terms like: **"FULL-BLEED composition," "fills the entire canvas from edge to edge (EVERY PIXEL),"** and **"STRICTLY EXCLUDE any borders, padding, fade-out, or vignette."**
    4. Output ONLY the final enhanced description string.
    """
    
    return system_instruction, user_prompt

# ----- story design -----
def get_story_designer_instructions(game_concept: str):
    SYSTEM_INSTRUCTION = f"""
    You are an expert Game Narrative and Visual Designer. Your task is to take a user's brief story concept and expand it into a detailed, structured creative brief for a slot machine or casual game, formatted ONLY as a JSON object.

    Strictly adhere to the following rules:

    1. **DO NOT** include any text, greetings, explanations, or code outside of the final JSON object.

    2. **STORYLINE:** Must be a concise narrative summary of the game's plot and theme, with a length of exactly 150 to 200 words.

    3. **SYMBOL COUNTS:** You MUST generate **exactly 3 High-Value Symbols**, **exactly 3 Mid-Value Symbols**, and **exactly 3 Low-Value Symbols**, plus one Wild and one Scatter. Do not deviate from these numbers.

    4. **DESCRIPTIONS:** All `appearance`, `background_personality`, and `description_for_generator` fields must be rich, detailed, and highly visual, adhering to the minimum length requirements specified in the schema.

    5. **SCENES:** You must create designs for both a `main_scene` and a distinct `freespin_scene`.

    6. **ENUM:** `symbol_type` must only use values: "High", "Mid", "Low", "Wild", or "Scatter".
    """

    # The user query is the actual prompt the user provides to generate the content.
    USER_PROMPT = f"""
    Design a full creative style guide for a new game based on this concept:

    **Concept:** {game_concept}
    """

    return SYSTEM_INSTRUCTION, USER_PROMPT