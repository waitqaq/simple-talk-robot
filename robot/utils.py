import os
import tempfile
def check_and_delete(src):
    """
    检查文件是否存在，如果存在进行删除
    """
    if os.path.exists(src):
        os.remove(src)

# 创建一个生成音频的技能
def write_temp_file(content, suffix):
    # 根据后缀产生一个随机的文件名，默认不删除
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        # 将content的内容写进去
        f.write(content)
        # 返回他的文件名
        tmpfile = f.name
    return tmpfile