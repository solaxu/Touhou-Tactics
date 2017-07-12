# Touhou-Tactics

A simple SLG exercise with Pygame for gaining Exp :p

My first time to try to build a real game demo.

Terrible coding coz...just typing, so you can find lots of Copy-Paste codes.

## BAD Programming Design Now:

1. A well designed Frame-Based Animation System is needed so that we can emit events at right time.

2. Finite State Machine System should support our Event Driven System. The response of events should be done in the states of an object.

3. The GUI System mixes both RMGUI and IMGUI, terrible.

4. The 2D rendering should be divided into layers.

5. The drawable objects should be organized as rendering queue so that they can remove themselves at right time to boost rendering effectiveness

6. Bad Object States design.

There are also many differences between the original Game Design(if there are design documents) and current version, such as the size of map, the economy system etc.


# Touhou-Tactics

第一次尝试写一个能玩的SLG demo，目前还处于初级阶段，主要是为了踩踩相关的坑 :p

代码写的乱，因为是边想边写的打补丁“修正主义”，有许多的粘贴代码，准备整体先走一遍。

## 目前踩到的坑：

1. 没有构建一个好的帧动画系统，以便于在播放动画的时候触发事件。

2. 有限状态机应当支持事件驱动，事件的响应应当下放到当前对象的状态中。

3. GUI 系统是由 Retained Mode GUI 与 Immediate Mode GUI 混着来的，不好。

4. 2D绘制没有进行分层，同时没有绘制物体队列。

5. 对象状态划分不好。

剩下的就是一些本身玩法设计上的事情了，比如关卡地图大小、经济系统等，正在考虑要不要砍掉装备系统。

虽然大体上是想搞个SLG，但是细节处在调试的时候就能感觉出来那些不对劲，只能慢慢踩慢慢调了。


# Screenshots:
![s](https://github.com/solaxu/Touhou-Tactics/blob/master/screenshot/01.png)
![s](https://github.com/solaxu/Touhou-Tactics/blob/master/screenshot/02.png)
![s](https://github.com/solaxu/Touhou-Tactics/blob/master/screenshot/03.png)
![s](https://github.com/solaxu/Touhou-Tactics/blob/master/screenshot/04.png)
![s](https://github.com/solaxu/Touhou-Tactics/blob/master/screenshot/05.png)
![s](https://github.com/solaxu/Touhou-Tactics/blob/master/screenshot/06.png)
![s](https://github.com/solaxu/Touhou-Tactics/blob/master/screenshot/07.png)
![s](https://github.com/solaxu/Touhou-Tactics/blob/master/screenshot/08.png)