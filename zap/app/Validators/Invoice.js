'use strict';

class Invoice {
  get rules() {
    return {
      client_id: 'required|integer',
      amount: 'required|number',
      description: 'string',
      due_date: 'required|date',
    };
  }

  get messages() {
    return {
      'client_id.required': 'Client is required',
      'client_id.integer': 'Invalid client ID',
      'amount.required': 'Amount is required',
      'amount.number': 'Amount must be a number',
      'due_date.required': 'Due date is required',
      'due_date.date': 'Invalid due date format',
    };
  }
}

module.exports = Invoice;