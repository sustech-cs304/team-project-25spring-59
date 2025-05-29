/// <reference types="cypress" />

describe('GymCourses 健身课程预定页面', () => {
  beforeEach(() => {
    // 设置模拟登录用户 ID
    cy.visit('http://localhost:5173/gym', {
      onBeforeLoad(win) {
        win.localStorage.setItem('user_id', '1') // 替换为实际测试 ID
      }
    })

    // 模拟点击进入某个 gym（例如 ID 为 101）
    cy.get('.el-card').first().click()

    // 确保加载成功
    cy.get('.el-table', { timeout: 10000 }).should('exist')
  })

  it('1. 页面加载后显示日期卡片和课程表', () => {
    cy.get('.el-card').should('have.length.at.least', 1) // 日期卡片
    cy.get('.el-table').should('exist') // 表格存在
    cy.get('.el-table .el-table__row').should('have.length.at.least', 1) // 至少一个课程行
  })




  it('2. 显示已预定状态的按钮不可点击', () => {
    cy.get('.el-table__row').each(($row) => {
      cy.wrap($row).within(() => {
        cy.get('button').then(($btn) => {
          const text = $btn.text()
          if (text.includes('已预定')) {
            cy.wrap($btn).should('be.disabled')
          }
        })
      })
    })
  })
})
