'use strict'


const Invoice = use('App/Models/Invoice');
const Client = use('App/Models/Client');

class InvoiceController {
  async index({ view }) {
    const invoices = await Invoice.query().with('client').fetch();
    return view.render('invoice._partial.index', { 
      invoices: invoices.toJSON() 
    });
  }

  async create({ view }) {
    const clients = await Client.all();
    return view.render('invoice.create-invoice', { 
      clients: clients.toJSON() 
    });
  }

  async store({ request, response }) {
    const { client_id, amount, description, due_date } = request.all();
    // Validate and create the invoice
    const invoice = await Invoice.create({
      client_id,
      amount,
      description,
      due_date,
    })

      session.flash({ successmessage: 'Invoice created successfully!' });
      return response.redirect(`/invoices/${invoice.id}`);
  }

  async show({ params, view }) {
    const invoice = await Invoice.find(params.id);
    return view.render('invoice.view-invoice', { 
      invoice: invoice.toJSON() 
    });
  }

  async edit({ params, view }) {
    const invoice = await Invoice.find(params.id);
    const clients = await Database.table('clients').select('id', 'name');
    return view.render('invoice.edit-invoice', { 
      invoice: invoice.toJSON(), clients 
    });
  }

  async update({ params, request, response, session }) {
    const data = request.only(['client_id', 'amount', 'description', 'due_date']);
    const invoice = await Invoice.find(params.id);

    try {
      invoice.merge(data);
      await invoice.save();
      session.flash({ successmessage: 'Invoice updated successfully!' });

      return response.redirect(`/invoices/${invoice.id}`);
    } catch (error) {
      session.withErrors(error.messages).flashAll();
      return response.redirect('back');
    }
  }

  async destroy({ params, response, session }) {
    const invoice = await Invoice.find(params.id);
    await invoice.delete();
    session.flash({ successmessage: 'Invoice deleted successfully!' });

    return response.redirect('/invoices');
  }
}

module.exports = InvoiceController;
