def register(app):
    from application.controllers import company
    from application.controllers import department
    from application.controllers import project
    from application.controllers import engineer
    from application.controllers import user
    from application.controllers import login
    from application.controllers import skill
    from application.controllers import business_category
    from application.controllers import pwchange
    from application.controllers import assigned_member
    from application.controllers import engineer_actual_result
    from application.controllers import project_attachment
    from application.controllers import attachment
    from application.controllers import billing
    from application.controllers import engineer_history

    app.register_blueprint(company.bp)
    app.register_blueprint(department.bp)
    app.register_blueprint(engineer.bp)
    app.register_blueprint(project.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(skill.bp)
    app.register_blueprint(business_category.bp)
    app.register_blueprint(pwchange.bp)
    app.register_blueprint(assigned_member.bp)
    app.register_blueprint(engineer_actual_result.bp)
    app.register_blueprint(project_attachment.bp)
    app.register_blueprint(attachment.bp)
    app.register_blueprint(billing.bp)
    app.register_blueprint(engineer_history.bp)
