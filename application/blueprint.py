def register(app):
    from application.controllers import dashboard
    from application.controllers import company
    from application.controllers import department
    from application.controllers import project
    from application.controllers import engineer
    from application.controllers import user
    from application.controllers import login
    from application.controllers import skill
    from application.controllers import business_category
    from application.controllers import pwchange
    from application.controllers import project_attachment
    from application.controllers import attachment
    from application.controllers import engineer_history
    from application.controllers import holiday
    from application.controllers import project_contract
    from application.controllers import project_result
    from application.controllers import project_billing
    from application.controllers import billing
    from application.controllers import project_payment
    from application.controllers import payment

    app.register_blueprint(dashboard.bp)
    app.register_blueprint(company.bp)
    app.register_blueprint(department.bp)
    app.register_blueprint(engineer.bp)
    app.register_blueprint(project.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(skill.bp)
    app.register_blueprint(business_category.bp)
    app.register_blueprint(pwchange.bp)
    app.register_blueprint(project_attachment.bp)
    app.register_blueprint(attachment.bp)
    app.register_blueprint(engineer_history.bp)
    app.register_blueprint(holiday.bp)
    app.register_blueprint(project_contract.bp)
    app.register_blueprint(project_result.bp)
    app.register_blueprint(project_billing.bp)
    app.register_blueprint(billing.bp)
    app.register_blueprint(project_payment.bp)
    app.register_blueprint(payment.bp)
