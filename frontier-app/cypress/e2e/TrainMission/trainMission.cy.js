/// <reference types="cypress" />

describe('TrainMission 页面 E2E 测试', () => {
  beforeEach(() => {
    cy.visit('http://localhost:5173/trainMission')
  });

  it('1. 页面背景与容器加载成功', () => {
    cy.get('.layout-wrapper').should('exist')
    cy.get('.background-color-layer').should('exist')
    cy.get('.background-image-layer').should('exist')
  });

  it('2. Banner 区域渲染正常', () => {
    cy.get('.banner-wrapper').should('exist')
    cy.contains('Hello, Vue').should('exist')
    cy.contains('Sensei’ TrainMission').should('exist')
  });

  it('3. Header 组件加载并包含 base 路径', () => {
    // 简单验证 Header 渲染了
    cy.get('header').should('exist') // 你也可以设置具体类名判断
  });

  it('4. 任务列表组件 PlanList 存在', () => {
    cy.get('.plans-container').children().should('have.length.greaterThan', 0)
  });

  it('5. SpinePlayer 动画组件加载', () => {
    // 你可以根据组件结构定制选择器
    cy.get('.layout-wrapper').find('canvas').should('exist')
  });
});
