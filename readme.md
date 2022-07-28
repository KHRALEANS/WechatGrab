## WECHAT GRAB 

- 功能：把微信 Mac 版的消息转发到邮箱
- 原理：AppleScript. 在 System Events 的背景下获取微信进程的UI elements
- 缺点：微信窗口需要保持打开，不能关闭屏幕
- 测试环境：macOS Monterey 12.4; Wechat Version 3.2.0 (19442)
- 微信语言：中/英
- 使用：
  1. 修改config/config.txt
  2. 运行grab_msg.scpt

### config 写法

- 紧挨每个字段另起一行填写相应的值。
- 需要接收消息的联系人，每个填写一行。
- 全英文，中文联系人填写拼音（先在微信中搜索测试，在能搜到的结果第一个即可）
- 字段：
  1. contacts: 联系人（非联系人不会接受消息）
  2. loop_interval: 获取消息间隔（单位sec）
  3. which_python: python 路径
  4. abs_path: 项目的绝对路径
  5. SENDER_USERNAME: 转发消息所使用的邮箱名称
  6. SENDER_PASSWORD: 邮箱账户密码（SMTP）
  7. RECEIVER: 接收消息所使用的邮箱名称