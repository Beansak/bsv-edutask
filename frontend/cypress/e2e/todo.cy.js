describe('Logging into the system', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
    let taskId
    let todoID
  
    function log_in(){
      cy.visit('http://localhost:3000')


      cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)
        cy.get('form')
            .submit()
    }
    
    before(function () {
      // create a fabricated user from a fixture
      cy.fixture('user.json')
        .then((user) => {
          cy.request({
            method: 'POST',
            url: 'http://localhost:5000/users/create',
            form: true,
            body: user
          }).then((response) => {
            uid = response.body._id.$oid
            name = user.firstName + ' ' + user.lastName
            email = user.email
          })
        })
    })
  
    before(function () {
      // create a task for the user
        log_in()


        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/tasks/create',
          form: true,
          body: {
          'title': "new task",
          'description': "description",
          'userid': uid,
          'url': "http://example.com",
          'todos': "DeleteTest",
          }

      })
      .then((response) => {
          console.log('Task created', response.body)
          taskId = response.body[0]._id.$oid;
          
          return cy.request({
          method: 'POST',
          url: 'http://localhost:5000/todos/create',
          form: true,
          body: {
            taskid: taskId,
            description: "TodoInit",
            done: false
          }
        })
        .then((response) => {
          todoID = response.body._id.$oid;
        });
          
      });

        
    });

    beforeEach(function () {
      // enter the main main page
      log_in() 
  })

    it("R8UC3: Delete todo", () => {
      cy.get('.container')
        .contains('.title-overlay', 'new task')
        .parents('a')
        .click()

      cy.get('.todo-list .todo-item')
        .contains('.editable', 'DeleteTest')
        .parent()
        .find('.remover')
        .click()

      log_in()

      cy.get('.container')
        .contains('.title-overlay', 'new task')
        .parents('a')
        .click()
        
      cy.get('.todo-list')
        .should('not.contain.text', 'DeleteTest')
    })

    
    it("R8UC1: ADD button disabled when nothing written in add todo input", () => {
        cy.get('.container')
        .contains('.title-overlay', 'new task')
        .parents('a')
        .click()

        //enters todo

        cy.get('.todo-list')
        .find('.inline-form')
        .find('input[type=text]')
        
        //press button named "add" to add todo
        .get('.inline-form input[value="Add"]')
        .should('be.disabled')
    })

    it("R8UC2: Toggle todo to done", () => {
      
      cy.get('.container')
        .contains('.title-overlay', 'new task')
        .parents('a')
        .click()

      cy.request({
        method: 'PUT',
        url: `http://localhost:5000/todos/byid/${todoID}`,
        form: true,
        body: {
          data: JSON.stringify({'$set': {'done': false}})
        }
      });

      cy.get('.todo-list .todo-item')
        .contains('.editable', 'TodoInit')
        .parent()
        .find('.checker.unchecked')
        .click()

      cy.request({
        method: 'GET',
        url: `http://localhost:5000/todos/byid/${todoID}`,
      }).then((response) => {
        expect(response.body.done).to.be.true;
      });
    })

    it("R8UC2: Toggle todo to not done", () => {
      cy.get('.container')
        .contains('.title-overlay', 'new task')
        .parents('a')
        .click()

      cy.request({
        method: 'PUT',
        url: `http://localhost:5000/todos/byid/${todoID}`,
        form: true,
        body: {
          data: JSON.stringify({'$set': {'done': true}})
        }
      });

      cy.get('.todo-list .todo-item')
        .contains('.editable', 'TodoInit')
        .parent()
        .find('.checker.checked')
        .click()

      cy.request({
        method: 'GET',
        url: `http://localhost:5000/todos/byid/${todoID}`,
      }).then((response) => {
        expect(response.body.done).to.be.false;
      });
    })

    
    it('R8UC1: Enters todo', () => {
      
        cy.get('.container')
        .contains('.title-overlay', 'new task')
        .parents('a')
        .click()

        //enters todo

        cy.get('.todo-list')
        .find('.inline-form')
        .find('input[type=text]')
        .type('new todo')
        
        //press button named "add" to add todo
        .get('.inline-form input[value="Add"]')
        .click()
        
        
        //assert that the todo is now in the list
        cy.get('.todo-list')
        .should('contain.text', 'new todo')


    })
  
    after(function () {
      // clean up by deleting the user from the database
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
      }).then((response) => {
        cy.log(response.body)
      
      })
    })
  })