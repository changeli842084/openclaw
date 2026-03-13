// 测试飞书文档创建
const { feishu_doc } = require('/home/lcc/.npm-global/lib/node_modules/openclaw/extensions/feishu/skills/feishu-doc/dist/index.js');

async function main() {
  try {
    // 创建文档
    const result = await feishu_doc({
      action: 'create',
      title: '测试文档',
      owner_open_id: 'ou_516fc2a2b118d27565c34dcb2f3dcfa8'
    });
    console.log('创建结果:', JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('错误:', error);
  }
}

main();
