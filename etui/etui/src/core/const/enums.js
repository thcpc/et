

const GlobalConst = Object.freeze({
  UnKnown: Object.freeze({
    ID: -999,
    STR: 'UnKnown',
    EMPTY: '',
    Int: -999,
  }),
  ErrCode: Object.freeze({
    InvalidToken: -102,
    TokenTimeOut: -103,
  })
})

// const UnKnown = Object.freeze({
//   ID: -999,
//   STR: 'UnKnown',
//   EMPTY: '',
//   Int: -999,
// })


const etDocumentConst = Object.freeze({
  FullText: 'FullText',
  PlantUml: 'PlantUml',
  Business: 'business',
  Function: 'function',
  DocTab : Object.freeze({
    All: 1,
    User: 2,
    Task: 3,
  }),
  TaskType : Object.freeze({
    AssignAutoTask: '0',
    LinkAutoTask: '1',
    ExecuteAutoTask: '2',
    ExecuteRegressionTask: '3'
  })
})

// const Constant = Object.freeze({
//   FullText: 'FullText',
//   PlantUml: 'PlantUml',
// })

// const ErrCode = Object.freeze({
//   InvalidToken: -102,
//   TokenTimeOut: -103,
// })

// const DocTab = Object.freeze({
//   All: 1,
//   User: 2,
//   Task: 3,
// })
//
// const CategoryType = Object.freeze({
//   Business: 'business',
//   Function: 'function',
// })
//
// const TaskType = Object.freeze({
//   AssignAutoTask: '0',
//   LinkAutoTask: '1',
//   ExecuteAutoTask: '2',
//   ExecuteRegressionTask: '3'
// })

export { GlobalConst,etDocumentConst }
