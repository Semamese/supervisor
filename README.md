AI hand recognizer

## LOG 

### 2025.3.24
功能基本完备，能用了，只需要调优参数就可以达到一个更好的使用体验。

但是问题也就是我没有很好的调优参数，所以点击识别还不是很灵敏

### 2025.4.23

第一次尝试使用一个简单的二分Classifier作为左击的判断，基于我的手部采样了1000个未点击和1000个点击的帧

基于食指根部到小指根部的距离，手掌三点三角形面积，以及食指尖到拇指尖的距离 的二次项进行的classification任务，

准确率0.89， 使用上只要手不要离得太远，体验感比原先强很多

如果换成别人的手基于我手掌进行测试的结果未知。 如果更差可以考虑每次程序启动前进行一个采样，个人测试采样时间只需要10秒左右，尚且对于开发者来说可以接受。

也可以收集更多人的手部信息进行学习。

## 使用以及原理说明

我用的是外置摄像头，故而在24: cap = cv2.VideoCapture(1) 这里设了1。 数字代表着是你电脑里的哪个摄像头，自己调整一下如果报错

手掌深度用的是食指指根和小指指根的距离，这个是用来计算点击识别阈值的。这是一个线性模型，可能（其实确实）很不精确，未来可以考虑用手掌面积换成一个二元模型

滤波使用的是一欧元滤波算法

**所有动作基于右手**

左击：食指指尖和拇指指尖并拢，食指捏住
右击：小指指尖和拇指指尖并拢，小指捏住
拖拽：中指指尖和拇指指尖并拢为按下左键，移动改变鼠标位置，再次松开为拖拽结束， 中指捏住
推出：拇指指尖与小指指根重合，做4的手势就可以

## 当前不足

点击动作尚不够精准，可以优调threshold中的参数

晃动还是很厉害，考虑加强滤波算法或者更换滤波算法

### 更新方向

为了更稳定的找到识别点击的threshold， 可以更换手掌深度的参数（当前是食指根部到拇指根部的距离，可能不够精确）

特异化的话可以打开摄像头保持一个点击动作进行1000次采样（高效且不累人），然后使用机器学习计算对于该用户手指的最优参数，但是这样就会太特异化导致适配性不高。不可能针对每一个用户的手都在使用前进行一次机器学习。

但是这不失为一个小方向，如果我们能够找到一个更有适配性的机器学习模型的话。

未来大方向可以考虑用神经网络识别不同手势的图然后逐帧进行判断，这样的精确度肯定是大于一个简单的数学模型的

还有一个大问题就是，我当前尚未测试这个软件的开销，我本地使用的是i7 13600H， 32G DDR4 内存， logitech Brio Stream。 如此在识别循环中已经能感受出掉帧问题了。可能我们的算法还能优化。

除了左击右击和拖拽之外，可以考虑加上滚轮，以及更多定制化内容，比如复制粘贴截图等手势

还可以考虑开放一个用户自定义接口，实现方式我目前没想法。

### 加入配置环节

在这个环节里，本质就是根据不同人手掌的生物特性寻找点击的threshold，保证对每个用户来说点击都是精确识别的。

1. 统计三张left click 手指距离和食指根部到小指根部的距离的比例， 这个过程最好是三张不同的手掌深度， 从而获得一个定制化的点击threshold


# English Below


## Current Progress
The functionality is mostly complete and usable. All that's left is to fine-tune the parameters to achieve a better user experience.

The issue, however, is that I haven't done much parameter tuning yet, so click recognition isn't very sensitive at the moment.

## Usage and Explanation of Principles
You can use the provided virtual environment (venv) directly — no additional setup is needed.

I'm using an external webcam, so in line 24: cap = cv2.VideoCapture(1), the 1 refers to the camera index on your system. You may need to change this number depending on your setup — if it throws an error, try 0 or other values.

For estimating hand depth, I'm using the distance between the base of the index finger and the base of the pinky. This value is used to dynamically calculate the click detection threshold. It's based on a linear model, which is (actually) quite imprecise. In the future, we could consider switching to using palm area and implementing a two-variable model instead.

For smoothing, I'm using the One Euro Filter algorithm.

**All gestures are based on the right hand.**

Left click: Bring the index fingertip and thumb fingertip together (pinch with the index finger).

Right click: Bring the pinky fingertip and thumb fingertip together (pinch with the pinky).

Drag: Pinch with the middle finger and thumb to press the left mouse button, then move your hand to drag the cursor. Releasing ends the drag.

Exit: Bring the thumb fingertip and the base of the pinky together (a "4" gesture) to exit the program.

## Current Limitations
The click action is still not accurate enough — the threshold parameters could be further tuned.

Hand jitter is still quite noticeable. It may be worth strengthening or replacing the filtering algorithm.

### Future Improvements
To more reliably determine the click detection threshold, we could consider switching to a different measure of hand depth. Currently, we use the distance between the base of the index finger and the base of the thumb, which may not be precise enough.

A more specialized approach could involve having the user perform a click gesture in front of the camera and collecting 1000 samples. This would be efficient and not too tiring. Then we could use machine learning to calculate the optimal threshold for that specific user's fingers. However, this approach is too user-specific and lacks generalizability — it's unrealistic to train a model for each new user.

That said, it's still a potential direction. If we can develop a machine learning model with better generalization, it might be worth exploring.

A more ambitious approach would be to use a neural network to recognize hand gesture images frame by frame. This would undoubtedly be more accurate than a simple mathematical model.

Another major issue is that I haven’t yet tested the performance impact of the software. I'm currently running it on an i7-13600H with 32GB DDR4 memory and a Logitech Brio Stream webcam. Even with this hardware, I can already feel frame drops within the recognition loop. This suggests that the algorithm could still be optimized.

Besides left click, right click, and dragging, we could consider adding scroll wheel support and more customizable actions such as copy, paste, and screenshot gestures.

We could also consider exposing a user-defined interface — though I currently don’t have a concrete idea for how to implement that.

### Configuration Phase
The core idea of this phase is to determine the click threshold based on individual users' hand characteristics, ensuring accurate click detection for each person.

1. Collect three samples of the left-click gesture, measuring the distance between the clicking fingers and the distance from the base of the index finger to the base of the pinky.

2. These three samples should ideally be taken at different hand depths (distances from the camera), allowing us to obtain a personalized ratio between finger distance and hand size.

3. Based on this ratio, calculate a customized click threshold that better fits the user's natural hand gestures and improves detection accuracy.