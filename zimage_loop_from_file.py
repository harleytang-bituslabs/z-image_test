import os
import time
import datetime
import re

import torch
from diffusers import ZImagePipeline

# ===== 配置区域 =====
MODEL_ID = "Tongyi-MAI/Z-Image-Turbo"
PROMPT_FILE = "prompts.txt"        # 同目录下的 prompt 文件
OUTPUT_DIR = "output"              # 生成图片输出目录

DEFAULT_HEIGHT = 1024
DEFAULT_WIDTH = 1024
NUM_STEPS = 9                      # 官方推荐 9 步
GUIDANCE_SCALE = 0.0               # Turbo 必须为 0
SEED = None                          # 固定随机种子，方便对比效果；为 None 则每次随机
OUTPUT_NUM = 3                     # 每个 prompt 生成的图片数量
# ====================


def slugify(text: str, max_len: int = 40) -> str:
    """
    把 prompt 截断并转为适合做文件名的短描述
    """
    text = text.strip()
    if len(text) > max_len:
        text = text[:max_len]
    # 替换不适合作为文件名的字符
    text = re.sub(r"[^\w\-一-龥]+", "_", text)  # 保留中文、字母数字、下划线和-
    text = re.sub(r"_+", "_", text)
    return text.strip("_") or "image"

def parse_size(size_str: str):
    """
    解析 '宽x高' 或 '宽X高' 格式，例如 '1024x1344'.
    如果解析失败，返回 (DEFAULT_WIDTH, DEFAULT_HEIGHT).
    """
    size_str = size_str.strip().lower()
    m = re.match(r"^(\d+)\s*[Xx×]\s*(\d+)$", size_str)
    if not m:
        return DEFAULT_WIDTH, DEFAULT_HEIGHT
    w = int(m.group(1))
    h = int(m.group(2))
    # 简单保险：防止输错 0 或太小
    if w <= 30 or h <= 30:
        return DEFAULT_WIDTH, DEFAULT_HEIGHT
    return w, h

def load_prompts(path: str):
    """
    从 prompts.txt 读取多条配置：
    每一行格式：
        1024x1344 || prompt 文本
    - 尺寸必须写在左边
    - 空行、以 # 开头的行会被忽略
    返回：[{ "prompt": str, "width": int, "height": int }, ...]
    """
    if not os.path.exists(path):
        print(f"[WARN] Prompt 文件不存在：{path}")
        return []

    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw:
                continue
            if raw.startswith("#"):
                continue

            # 按 '||' 分割：左边尺寸，右边 prompt
            if "||" in raw:
                size_part, prompt_part = raw.split("||", 1)
                size_part = size_part.strip()
                prompt = prompt_part.strip()
                w, h = parse_size(size_part)
            else:
                # 如果用户忘写尺寸，则使用默认尺寸
                prompt = raw
                w, h = DEFAULT_WIDTH, DEFAULT_HEIGHT

            if not prompt:
                continue

            items.append({
                "prompt": prompt,
                "width": w,
                "height": h,
            })

    return items

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(">> Loading Z-Image-Turbo pipeline (bf16, no offload)...")
    pipe = ZImagePipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,   # 官方推荐：bf16
        low_cpu_mem_usage=True,      # 可选：节省 CPU 内存
    )
    pipe.to("cuda")
    pipe.set_progress_bar_config(disable=True)
    print(">> Pipeline loaded and moved to CUDA.")

    print(f"\n使用说明：")
    print(f"- 在当前目录创建/编辑 {PROMPT_FILE}，每一行一条任务：")
    print(f"    prompt 文本 || 1024x1024")
    print(f"  例如：A cute shiba inu astronaut || 768x1024")
    print(f"- '|| 尺寸' 部分可以省略，省略时使用默认分辨率 {DEFAULT_WIDTH}x{DEFAULT_HEIGHT}。")
    print(f"- 图片会保存在 {OUTPUT_DIR}/ 下，命名：时间戳 + 截断后的描述。")
    print(f"- 每次修改 {PROMPT_FILE} 后，回到程序按回车，就会重新读取文件并生成。")
    print(f"- 输入 q 回车可以退出程序。\n")

    while True:
        cmd = input("按回车开始本轮生成（或输入 q 回车退出）：").strip().lower()
        if cmd in {"q", "quit", "exit"}:
            print("退出程序。")
            break

        items = load_prompts(PROMPT_FILE)
        if not items:
            print(f"[WARN] 没有在 {PROMPT_FILE} 中读到有效内容（可能是空文件或只有注释）。")
            continue

        print(f"\n本轮共 {len(items)} 条任务，将逐条生成：\n")

        for idx, item in enumerate(items, start=1):
            prompt = item["prompt"]
            width = item["width"]
            height = item["height"]

            print(f"[{idx}/{len(items)}] prompt: {prompt}")
            print(f"    size: {width}x{height}")

            generator = None
            if SEED is not None:
                generator = torch.Generator("cuda").manual_seed(SEED)

            t0 = time.time()
            out = pipe(
                prompt=prompt,
                height=height,
                width=width,
                num_inference_steps=NUM_STEPS,
                guidance_scale=GUIDANCE_SCALE,
                generator=generator,
                num_images_per_prompt=OUTPUT_NUM,
            )
            t1 = time.time()

            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            slug = slugify(prompt)

            for i, image in enumerate(out.images):
                filename = f"{ts}_{width}x{height}_{slug}_{i+1}.png"
                save_path = os.path.join(OUTPUT_DIR, filename)
                image.save(save_path)
                print(f"  -> 保存到 {save_path}")

            print(f"总用时 {t1 - t0:.2f} 秒\n")

if __name__ == "__main__":
    main()