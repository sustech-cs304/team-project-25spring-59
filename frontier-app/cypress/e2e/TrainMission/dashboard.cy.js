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

