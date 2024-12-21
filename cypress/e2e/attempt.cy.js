/* eslint-disable no-undef */
describe('Attempt Testing', () => {
  it('passes', () => {
    cy.visit('http://180.250.135.10/moodle')
    // cy.get('a[href*="login"]').click()
    cy.get('.login').find('a').click()
    cy.wait(2000)
    cy.get('input#username').focus().type('moodledude_user')
    cy.get('input#password').focus().type('Moodle_user_1')
    cy.get('button#loginbtn').click()
  })
})
