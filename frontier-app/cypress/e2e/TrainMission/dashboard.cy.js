/// <reference types="cypress" />
Cypress.on('uncaught:exception', (err) => {
  if (err.message.includes("AudioBufferSourceNode")) {
    return false; // 阻止 Cypress 失败
  }
   // 忽略音频错误
  if (err.message.includes("AudioBufferSourceNode")) return false;

  // 忽略 undefined.length 错误
  if (err.message.includes("Cannot read properties of undefined (reading 'length')")) return false;
});


describe('Dashboard 页面 E2E 测试', () => {
  beforeEach(() => {
    // 设置用户 ID，必须在 visit 前设置
    cy.window().then((win) => {
      win.localStorage.setItem('user_id', '1') // 使用模拟 ID 或有效 ID
    })

    cy.visit('http://localhost:5173/TrainMission/Dashboard')
  })

  it('1. 页面基础结构加载成功', () => {
    cy.get('.layout-wrapper').should('exist')
    cy.get('.background-color-layer').should('exist')
    cy.get('.background-image-layer').should('exist')
  })

  it('2. 用户训练汇总卡片正确渲染', () => {
    cy.get('.stats-summary-cards').should('exist')
    cy.get('.cards-container .stat-card').should('have.length', 5)

    const labels = ['总训练时长', '估算卡路里', '实际卡路里', '平均心率', '最大心率']
    labels.forEach(label => {
      cy.contains('h4', label).should('exist')
    })
  })

  it('3. 图表组件渲染成功', () => {
    cy.get('.chart-container').should('exist')
  })


})


/// <reference types="cypress" />

describe('Dashboard 页面 AI 助手面板显示/关闭测试', () => {
  beforeEach(() => {
    // 设置用户 ID，必须在 visit 前设置
    cy.window().then((win) => {
      win.localStorage.setItem('user_id', '1') // 使用模拟 ID 或有效 ID
    })

    cy.visit('http://localhost:5173/TrainMission/Dashboard');
  });

  it('AI 训练助手面板可显示与关闭', () => {
    cy.visit('http://localhost:5173/TrainMission/Dashboard', {
      onBeforeLoad(win) {
        win.localStorage.setItem('user_id', '1')
      }
    })

    // 等待 window 上挂载 setAISidebarVisible 函数（最多重试10秒）
    cy.window().should((win) => {
      expect(typeof win.setAISidebarVisible).to.equal('function')
    })

    // 然后再安全调用
    cy.window().then((win) => {
      win.setAISidebarVisible(true)
    })

    // 验证 AI 面板出现
    cy.get('.ai-float-sidebar', { timeout: 5000 }).should('exist').and('be.visible')

    // 点击关闭按钮
    cy.get('.ai-header button').click()

    // 验证面板消失
    cy.get('.ai-float-sidebar').should('not.exist')
  })
});

/// <reference types="cypress" />

describe('AI 助手面板输入交互测试', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173/TrainMission/Dashboard', {
      onBeforeLoad(win) {
        win.localStorage.setItem('user_id', '1')
      }
    })

    // 等待 setAISidebarVisible 可用
    cy.window().should('have.property', 'setAISidebarVisible')

    // 显示面板
    cy.window().then((win) => {
      win.setAISidebarVisible(true)
    })

    cy.get('.ai-float-sidebar', { timeout: 5000 }).should('exist').and('be.visible')
  })

  it('在 AI 输入框中输入问题并接收到回复', () => {
    const userInput = '请帮我生成下周训练计划'

    // 输入用户问题
    cy.get('.ai-input input')
      .should('exist')
      .type(userInput)

    // 点击发送按钮
    cy.get('.ai-input button').click()

    // 验证用户输入是否展示在消息中
    cy.contains('.chat-message.user .bubble', userInput).should('exist')

    // 验证 assistant 回复出现（等待最长 20s）
    cy.get('.chat-message.assistant .bubble', { timeout: 20000 })
      .should('exist')
      .and('not.contain', '[获取失败]')
      .and('not.contain', 'AI 无响应')

    // 可选：验证包含关键词（用于区分 task/chat）
    // cy.get('.chat-message.assistant .bubble').should('contain.text', '训练计划')
  })
})


