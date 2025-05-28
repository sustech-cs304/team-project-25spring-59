Cypress.on('uncaught:exception', (err, runnable) => {
  // 忽略 AudioBufferSourceNode 相关异常
  if (err.message.includes("Failed to set the 'buffer' property on 'AudioBufferSourceNode'")) {
    return false // 阻止 Cypress 抛出异常
  }
})

describe('用户登录流程', () => {
  beforeEach(() => {
    // 访问登录页面（确保你已启动前端 dev 服务器）
    cy.visit('http://localhost:5173/login')
  })

  it('点击进入登录界面，并显示登录表单', () => {
    // 初始状态：登录卡片不存在
    cy.get('.login-card').should('not.exist')

    // 点击触发显示登录表单
    cy.get('.login-container').click()

    // 登录卡片出现
    cy.get('.login-card').should('exist')
  })

  it('输入用户名和密码后点击登录，模拟登录请求', () => {
    cy.intercept('POST', '**/api/login', {
      statusCode: 200,
      body: {
        message: '登录成功',
        token: 'mock-token',
        user_id: 123
      }
    }).as('loginRequest');

    cy.visit('http://localhost:5173/login');
    cy.get('.login-container').click();

    cy.get('input[placeholder="请输入用户名"]').type('user1');
    cy.get('input[placeholder="请输入密码"]').type('password1');

    cy.contains('用户登录').click();

    // ✅ 验证页面是否出现成功提示
    cy.get('.el-message')
      .should('be.visible')
      .and('contain.text', '登录成功');
  });



  it('未填用户名/密码时应提示错误', () => {
    cy.get('.login-container').click()
    cy.contains('用户登录').click()

    cy.get('.el-message').should('contain.text', '请输入用户名和密码')
  })
})
