# comfyui
介绍K采样器
- 随机种：图片的身份证，如果固定，图片是不会再变的
- 步长（40以内）：消除图片噪点次数。类似于擦玻璃
- CFG（5～8）：匹配程度。越高越匹配
- 采样器：控制降噪的程度。dpmpp_2m、dpmpp_2m_sde表现较好
- 调度器：控制降噪的方法。karras
- 降噪：数值越高，噪点越多，图片越偏离
图片--》vae加载器（选择模型）--〉vae编码器--》vae解码器

```
clip编码器
描述质量词汇+主体词汇+氛围环境词汇（高清，女孩，花园）
```

## controlnet
controlnet加载器（选择模型）--》controlnet应用
##### canny

##### softedge
controlnet加载器中的模型更换为softedge模型
图片的预处理器更换为softedge（HED）
软边缘，基于线条边缘更多的发挥空间
##### lineart
线稿上色，图像（可以通过get image size节点自动知道图片大小，将空laternt的宽高右键转为输入）--》lineart节点
##### openpose
基于姿势和面部
controlnet加载器中的模型更换为openpose模型
图片的加载器更换为openpose预处理节点（DW姿态处理器）
##### Depth
深度控制模型
基于空间
controlnet加载器中的模型更换为depth模型
图片的加载器更换为depth预处理节点（Zoe深度预处理器）

## IPAdapter FaceID换脸模型

# Wan2.2_12V_A14B图生视频模型
工作了--》模版--〉video--》选择模型