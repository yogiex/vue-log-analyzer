describe('Attempt Testing', () => {
  it('passes', () => {
    cy.visit('http://180.250.135.10/moodle')
    cy.get('a[href*="login"]').click()
  })
})
