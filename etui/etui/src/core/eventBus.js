

import { reactive, readonly } from 'vue';

const state = reactive({
    events: new Map()
});

const emit = (event, payload) => {
    const callbacks = state.events.get(event);
    if (callbacks) {
        callbacks.forEach(callback => callback(payload));
    }
};

const on = (event, callback) => {

    const callbacks = state.events.get(event);
    if (!callbacks) {
        state.events.set(event, [callback]);
    } else {
        callbacks.push(callback);
    }

    return () => {
        off(event, callback);
    };
};

const off = (event, callback) => {
    const callbacks = state.events.get(event);
    if (callbacks) {
        const index = callbacks.indexOf(callback);
        if (index !== -1) {
            callbacks.splice(index, 1);
        }
    }
};

export const EventBus = {
    $on: on,
    $emit: emit,
    $off: off,
    // 提供一个只读的 state，用于在严格模式下避免直接修改
    $state: readonly(state)
};

export default EventBus;
