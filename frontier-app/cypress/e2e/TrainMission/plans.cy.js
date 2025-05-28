/// <reference types="cypress" />

describe('Plans 页面 E2E 测试', () => {
  beforeEach(() => {
    // 设置用户ID，必须在 visit 前完成
    cy.window().then((win) => {
      win.localStorage.setItem('user_id', '1')
    })

    // 访问页面（确保 localStorage 已设定）
    cy.visit('http://localhost:5173/TrainMission/Plans')
  })

  it('1. 页面主结构和背景渲染成功', () => {
    cy.get('.layout-wrapper').should('exist')
    cy.get('.background-color-layer').should('exist')
    cy.get('.background-image-layer').should('exist')
  })

  it('2. weekly-plan 组件加载成功', () => {
    cy.get('.weekly-plan').should('exist')
    cy.get('.task-panel-container').should('exist')
  })

  it('3. 日期范围正确显示', () => {
    cy.get('.date-range').should('exist').and('include.text', '年')
  })

  it('4. 七天任务面板都存在', () => {
    cy.get('.task-panel-container .task-panel').should('have.length', 7)
  })

  it('5. 点击下一周，日期范围会变化', () => {
    cy.get('.date-range').invoke('text').then((originalText) => {
      cy.contains('下一周').click()
      cy.wait(1000)
      cy.get('.date-range').invoke('text').should('not.eq', originalText)
    })
  })

  it('6. 点击上一周，日期范围也会变化', () => {
    cy.get('.date-range').invoke('text').then((originalText) => {
      cy.contains('上一周').click()
      cy.wait(1000)
      cy.get('.date-range').invoke('text').should('not.eq', originalText)
    })
  })

  it('7. 每天的任务内容是否加载成功', () => {
    // 任务是异步加载，需等待加载完成
    cy.wait(2000)

    cy.get('.task-panel-container .task-panel').each(($panel) => {
      cy.wrap($panel).within(() => {
        cy.get('li').should('exist') // 每个面板应至少有一个任务 li 元素
      })
    })
  })
})
