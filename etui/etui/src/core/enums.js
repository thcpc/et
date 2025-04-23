const UnKnown = Object.freeze({
  ID: -999,
  STR: 'UnKnown',
  EMPTY: '',
  Int: -999,
})

const Constant = Object.freeze({
  FullText: 'FullText',
  PlantUml: 'PlantUml',
})

const ErrCode = Object.freeze({
  InvalidToken: -102,
  TokenTimeOut: -103,
})

const DocTab = Object.freeze({
  All: 1,
  User: 2,
  Task: 3,
})

const CategoryType = Object.freeze({
  Business: 'business',
  Function: 'function',
})

const TaskType = Object.freeze({
  AssignAutoTask: '0',
  LinkAutoTask: '1',
  ExecuteAutoTask: '2',
  ExecuteRegressionTask: '3'
})

export { UnKnown, Constant, ErrCode, DocTab, CategoryType, TaskType}
