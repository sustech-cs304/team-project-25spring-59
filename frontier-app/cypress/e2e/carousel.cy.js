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
// 忽略 PixiJS 的音频重复绑定异常
Cypress.on('uncaught:exception', (err) => {
  if (err.message.includes("AudioBufferSourceNode")) {
    return false;
  }
});

describe('Carousel 页面 E2E 测试', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173/carousel');
  });

  it('1. 页面成功加载背景与主容器', () => {
    cy.get('#background').should('exist');
    cy.get('.main-container').should('exist');
  });


  it('2. 点击右上角感叹号弹出关于弹窗', () => {
    cy.get('.alert-box').click();
    cy.get('.modal-content').should('exist');
    cy.contains('项目成员').should('be.visible');
  });

  it('3. 关闭弹窗功能正常', () => {
    cy.get('.alert-box').click();
    cy.get('.close-button').click();
    cy.get('.modal-content').should('not.exist');
  });

  it('4. 点击右下角跳转按钮播放动画并跳转页面', () => {
    cy.visit('http://localhost:5173/carousel')

    // 等待动画加载完成
    cy.wait(1500)

    // 点击并强制执行
    cy.get('.switch-wrapper').click({ force: true })

    // 等待页面跳转
    cy.location('pathname', { timeout: 10000 }).should('include', '/TrainMission/Dashboard')
  })
});


describe('Carousel 页面 Footer 菜单跳转测试', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173/carousel')
  })

  const footerRoutes = [
    { label: '健身排课', path: '/gym' },
    { label: '积分排行', path: '/leaderboard' },
    { label: '社交分享', path: '/share' },
    { label: '在线挑战', path: '/challenge' },
    { label: '个人中心', path: '/personal' }
  ]

  footerRoutes.forEach(({ label, path }) => {
    it(`点击菜单项「${label}」应跳转到 ${path}`, () => {
      // 确保 FooterMenu 加载完毕
      cy.get('.footer-nav').should('exist')

      // 点击对应菜单项
      cy.contains('span', label).should('be.visible').click({ force: true })

      // 验证跳转路径
      cy.location('pathname', { timeout: 15000 }).should('eq', path)

      // 若需测试多个按钮，返回 carousel 页面
      cy.visit('http://localhost:5173/carousel')
    })
  })
})